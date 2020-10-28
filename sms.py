import subprocess
import fileinput as fi

solver = '../open-wbo/open-wbo'

n = 0

# Initiliaze tasks' data arrays(TODO nasty -1)
r = [-1]
p = [-1]
d = [-1]
nk = [-1]
k = [[]]
deps = [[]]

# Get data from .sms file
for line in fi.input():
    if fi.isfirstline():
        n = int(line)
    # TODO talvez tirar ifs
    elif fi.filelineno() <= n+1:
        line = line.split()
        r.append(int(line[0]))
        p.append(int(line[1]))
        d.append(int(line[2]))
        nk.append(int(line[3]))
        k.append([int(k) for k in line[4:]])
    else:
        line = line.split()
        if line[0] == 0:
            deps.append([])
        else:
            deps.append([int(dep) for dep in line[1:]])

# Construct dictionaries for variables/literal mapping
lit = 1
getlit = {}
getvar = {}

for i in range(1,n+1):
    getlit[('t',i)] = lit
    getvar[lit] = ('t',i)
    lit += 1

for i in range(1,n+1):
    for j in range(1, nk[i]+1):
        for t in range(r[i], d[i]):
            getlit[('k',i,j,t)] = lit
            getvar[lit] = ('k',i,j,t)
            lit += 1



print('getlit: ')
print(getlit)
print('getvar: ')
print(getvar)

################
# HARD CLAUSES #
################

hardclauses = []

# Fragments must be processed in order
for i in range(1, n+1):
    for j in range(2, nk[i]+1):
#        -(k,i,j) \/ (k,i,j-1)
        pass

################
# SOFT CLAUSES #
################

softclauses = []

for task in range(1,n+1):
    softclauses.append([task])

# Convert to wcnf
cnf = 'p wcnf ' + str(n) + ' ' + str(n) + ' ' + str(n + 1) + '\n'

for c in softclauses:
    cnf += '1 ' + str(c[0]) + ' 0\n'

# Run
print(cnf)
solution = subprocess.run(solver, input=bytes(cnf, encoding='utf-8'))
print(solution)