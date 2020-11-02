import subprocess
import fileinput as fi

solver = '../open-wbo/open-wbo'

######################
# TASKS' DATA ARRAYS #
######################

# !! HACK we initialized the 0th entry of each array so we could reference tasks by their number regarding the problem specification !!
# !! e.g. task 1 release time can be accessed with r[1]                                                                              !!
nt = 0
r = [-1]
p = [-1]
d = [-1]
nk = [-1]
k = [[]]
deps = [[]]

# Get data from .sms file
for line in fi.input():
    if fi.isfirstline():
        nt = int(line)
    # TODO talvez tirar ifs
    elif fi.filelineno() <= nt+1:
        line = line.split()
        r.append(int(line[0]))
        p.append(int(line[1]))
        d.append(int(line[2]))
        nk.append(int(line[3]))
        k.append([-1] + [int(k) for k in line[4:]])
    else:
        line = line.split()
        if line[0] == 0:
            deps.append([])
        else:
            deps.append([int(dep) for dep in line[1:]])


#########################
# VARIABLE/LITERAL MAPS #
#########################

lit = 1
getlit = {}
getvar = {}

for i in range(1,nt+1):
    getlit[('t',i)] = lit
    getvar[lit] = ('t',i)
    lit += 1

for i in range(1,nt+1):
    for j in range(1, nk[i]+1):
        for t in range(r[i], d[i]):
            getlit[('k',i,j,t)] = lit
            getvar[lit] = ('k',i,j,t)
            lit += 1

print('mapa:')
for entry in getvar:
    print(entry, ':',getvar[entry])


################
# HARD CLAUSES #
################

hardclauses = []

# k must be processed in order
# K(i, j, t) => union [K(i, j-1, x)]    ,   forall( x < t ) forall(i, j)
# TODO optimize redundant clauses
for i in range(1, nt+1):
    for j in range(2, nk[i]+1):
        for t in range(r[i], d[i]):
            cl = [-1 * getlit[('k',i,j,t)]]
            for x in range(r[i], t):
                cl.append(getlit[('k',i,j-1,x)])
            hardclauses.append(cl)

# If a fragment starts its execution, it has to be executed until it is completed
# [K(i, j, t) and -K(i, j, t-1)] or K(i ,j, 0) -> K(i, j, x)    ,   forall(i, j, t)  forall( t < x < t + p(i, j) )
for i in range(1, nt+1):
    for j in range(1, nk[i]+1):
        for t in range(r[i], d[i]):
            if t == 0:
                for x in range(t+1, t + k[i][j]):
                    cl = [-1 * getlit[('k',i,j,0)], getlit[('k',i,j,x)]]
                    hardclauses.append(cl)
            elif t == r[i]:
                for x in range(t+1, t + k[i][j]):
                    cl = [-1 * getlit[('k',i,j,r[i])], getlit[('k',i,j,x)]]
                    hardclauses.append(cl)                
            else:
                for x in range(t+1, t + k[i][j]):
                    if x >= d[i]:
                        cl = [-1 * getlit[('k',i,j,t)], getlit[('k',i,j,t-1)]]
                    else:
                        cl = [-1 * getlit[('k',i,j,t)], getlit[('k',i,j,t-1)], getlit[('k',i,j,x)]]
                    hardclauses.append(cl)


# A task is completed if its last fragment is completed
# K(i, nk[i], t) => T(i),   where, forall (i, t)
for i in range(1, nt+1):
    # OPT minimum release
    minimumrelease = 0
    for j in range(1, nk[i]):
        minimumrelease += k[i][j]
    cll = [-1 * getlit[('t',i)]]
    for t in range(r[i]+minimumrelease, d[i]):
        clr = [ -1 * getlit[('k',i,nk[i],t)], getlit[('t',i)] ]
        cll.append(getlit[('k',i,nk[i],t)])
        hardclauses.append(clr)

    hardclauses.append(cll)

# Only one fragment can be processed at instant t (PAIRWISE ENCODING)
# sum [iterate on i,j]  K(i, j, t) <= 1 ,   forall(t)
for t in range(0, max(d)):
    conflictious = []
    for i in range(1, nt+1):
        if r[i] <= t and t < d[i]:
            for j in range(1, nk[i]+1):
                conflictious.append(getlit[('k',i,j,t)])
    print('conflictious: ', conflictious)
    for k in range(0, len(conflictious)):
        for conf in conflictious[(k+1):]:
            print([-1 * conflictious[k], -1 * conf])
            hardclauses.append([-1 * conflictious[k], -1 * conf])


################
# SOFT CLAUSES #
################

softclauses = []

for i in range(1, nt+1):
    softclauses.append([getlit[('t',i)]])


##################
# RUN SAT SOLVER #
##################

# Convert to wcnf
top = str(nt + 1)
cnf = 'p wcnf ' + str(nt) + ' ' + str(nt) + ' ' + top + '\n'

for c in hardclauses:
    cnf += top
    for lit in c:
        cnf += ' ' + str(lit)
    cnf += ' 0\n'

for c in softclauses:
    cnf += '1 ' + str(c[0]) + ' 0\n'

# Run
#print(cnf)
solution = str(subprocess.run(solver, input=bytes(cnf, encoding='utf-8'), capture_output=True).stdout, encoding='utf-8')

# Interpet solver output
print(solution)
cost = nt
model = []
for line in solution.split('\n'):
    linearray = line.split()
    if linearray != [] and linearray[0] == 'o':
        cost = int(linearray[1])
    elif linearray != [] and linearray[0] == 'v':
        model = list(map(int, linearray[1:]))

print(model)
for l in model:
    if l > 0:
        print(getvar[l])

# Print optimum number of processed tasks
output = ''
output += str(nt-cost) + '\n'

# For every task that is processed, print its fragments
for i in range(1, nt+1):
    taskinfo = ''
    if model[i-1] > 0:
        taskinfo += str(i)
        for j in range(1, nk[i]+1):
            for t in range(r[i], d[i]):
                if getlit[('k', i, j, t)] in model:
                    taskinfo += ' ' + str(t)
                    break
        taskinfo += '\n'
        output += taskinfo

print(output)