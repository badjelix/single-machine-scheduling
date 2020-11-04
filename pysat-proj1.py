from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
from pysat.card import *
import fileinput as fi
import math

solver = RC2(WCNF())

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



################
# HARD CLAUSES #
################

# k must be processed in order
# K(i, j, t) => union [K(i, j-1, x)]    ,   forall( x < t ) forall(i, j)
# TODO optimize redundant clauses
for i in range(1, nt+1):
    for j in range(2, nk[i]+1):
        for t in range(r[i], d[i]):
            cl = [-1 * getlit[('k',i,j,t)]]
            for x in range(r[i], t):
                cl.append(getlit[('k',i,j-1,x)])
            solver.add_clause(cl)


# If a fragment starts its execution, it has to be executed until it is completed
# [K(i, j, t) and -K(i, j, t-1)] or K(i ,j, 0) -> K(i, j, x)    ,   forall(i, j, t)  forall( t < x < t + p(i, j) )
for i in range(1, nt+1):
    for j in range(1, nk[i]+1):
        for t in range(r[i], d[i]):
            if t == 0 or t == r[i]:
                for x in range(t+1, t + k[i][j]):
                    cl = [-1 * getlit[('k',i,j,t)], getlit[('k',i,j,x)]]
                    solver.add_clause(cl)           
            else:
                for x in range(t+1, t + k[i][j]):
                    if x >= d[i]:
                        cl = [-1 * getlit[('k',i,j,t)], getlit[('k',i,j,t-1)]]
                    else:
                        cl = [-1 * getlit[('k',i,j,t)], getlit[('k',i,j,t-1)], getlit[('k',i,j,x)]]
                    solver.add_clause(cl)


# If a fragmant starts its execution, a fragment can’t be processed after its processing time
# [K(i, j, t) and -K(i, j, t-1)] or K(i, j, 0) -> -K(i, j, x)   ,   forall(i, j, t)  forall( t + p(i, j) >= x)
for i in range(1, nt+1):
    for j in range(1, nk[i]+1):
        for t in range(r[i], d[i]):
            if t == 0 or t == r[i]:
                for x in range(t + k[i][j], d[i]):
                    cl = [-1 * getlit[('k',i,j,t)], -1* getlit[('k',i,j,x)]]
                    solver.add_clause(cl)
            else:
                for x in range(t + k[i][j], d[i]):
                    cl = [-1 * getlit[('k',i,j,t)], getlit[('k',i,j,t-1)], -1 * getlit[('k',i,j,x)]]
                    solver.add_clause(cl)


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
        solver.add_clause(clr)

    solver.add_clause(cll)


# A task can only start if the tasks it depends on are already processed
# K(i, 1, t) => Ux K(c, nk[c], x) forall (i, t)
for i in range(1, nt+1):
    for t in range(r[i], d[i]):
        for c in deps[i]:
            cl = [-1 * getlit[('k', i, 1, t)]]
            limit = min(t, d[c])
            for x in range(r[c], limit):
                cl.append(getlit[('k', c, nk[c], x)])
            solver.add_clause(cl)


# # Only one fragment can be processed at instant t (PAIRWISE ENCODING)
# # sum [iterate on i,j]  K(i, j, t) <= 1 ,   forall(t)
# for t in range(0, max(d)):
#     conflictious = []
#     for i in range(1, nt+1):
#         if r[i] <= t and t < d[i]:
#             for j in range(1, nk[i]+1):
#                 conflictious.append(getlit[('k',i,j,t)])
#     for k in range(0, len(conflictious)):
#         for conf in conflictious[(k+1):]:
#             solver.add_clause([-1 * conflictious[k], -1 * conf])


# Only one fragment can be processed at instant t (PYSAT ENCODING)
# sum [iterate on i,j]  K(i, j, t) <= 1 ,   forall(t)
nvars = len(getlit)
max_var = nvars + 1
for t in range(0, max(d)):
    conflictious = []
    for i in range(1, nt+1):
        if r[i] <= t and t < d[i]:
            for j in range(1, nk[i]+1):
                conflictious.append(getlit[('k',i,j,t)])
    constraint = CardEnc.atmost(lits=conflictious, bound=1, top_id=max_var, encoding=EncType.bitwise)
    for clause in constraint.clauses:
        solver.add_clause(clause)
    max_var += math.ceil(math.log(len(conflictious)+1, 2))

################
# SOFT CLAUSES #
################

for i in range(1, nt+1):
    solver.add_clause([getlit[('t',i)]], weight = 1)

model = solver.compute()

output = ''
output += str(nt-solver.cost) + '\n'

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