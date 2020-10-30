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
# TODO optimize redundant clauses
for i in range(1, nt+1):
    for j in range(2, nk[i]+1):
        for t in range(r[i], d[i]):
            cl = [-1 * getlit[('k',i,j,t)]]
            for x in range(r[i], t):
                cl.append(getlit[('k',i,j-1,x)])

            hardclauses.append(cl)
            

# A task is completed if its last fragment is completed
# K(i, nk[i], t) => T(i),   where, forall (i, t)
for i in range(1, nt+1):
    # OPT minimum release
    minimumrelease = 0
    for j in range(1, nk[i]):
        minimumrelease += k[i][j]
    for t in range(r[i]+minimumrelease, d[i]):
        clr = [ -1 * getlit[('k',i,nk[i],t)], getlit[('t',i)] ]
        cll = [ -1 * getlit[('t',i)], getlit[('k',i,nk[i],t)] ]
        hardclauses.append(clr)
        hardclauses.append(cll)


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



print(str(nt-cost))
for i in range(1, nt+1):
    if model[i-1] > 0:
        output = str(i)
    print(output)