import fileinput as fi
from z3 import Solver
from z3 import Bool, Int, sat, IntVal
from z3 import Or, And, If, Distinct, Optimize, Implies


# HACK we initialized the 0th entry of each array so we could reference tasks by their number according the problem specification
# e.g. task 1 release time can be accessed with r[1]
nt = 0
r = [-1]
p = [-1]
d = [-1]
nk = [-1]
pk = [[]]
deps = [[]]


def read_input():
    global nt, r, p, d, nk, k, deps

    # Get data from .sms file
    for line in fi.input():
        if fi.isfirstline():
            nt = int(line)
        elif fi.filelineno() <= nt+1:
            line = line.split()
            r.append(int(line[0]))
            p.append(int(line[1]))
            d.append(int(line[2]))
            nk.append(int(line[3]))
            pk.append([-1] + [int(k) for k in line[4:]])
        else:
            line = line.split()
            if line[0] == 0:
                deps.append([])
            else:
                deps.append([int(dep) for dep in line[1:]])


def solve():
    solver = Optimize()

    T = [-1]
    K = [[]]

    for i in range(1, nt+1):
        T.append(Int(f'T({i})'))

    for i in range(1, nt+1):
        frags = [-1]
        for j in range(1, nk[i]+1):
            frags.append(Int(f'K({i}, {j})'))
        K.append(frags)

    # Task “flags” can only be assigned to 0 or 1 SERA Q É PRECISO???
    # T(i) >= 0    AND   T(i) <= 1
    for i in range(1, nt+1):
        solver.add(And(T[i] >= 0, T[i] <= 1))

    # Fragments can only be executing between their task's release and deadline
    # K(i,j) >= r(i) AND K(i,j) + p(i,j) < d(i)
    # FIXME: podem ser -1 ?
    for i in range(1, nt+1):
        for j in range(1, nk[i]+1):
            solver.add(And(K[i][j] >= r[i], K[i][j] + pk[i][j] < d[i]))


    if solver.check() == sat:
        model = solver.model()

        ### Testing ###
        for i in range(1, nt + 1):
            print(f'T({i}): {model[T[i]]}')

        for i in range(1, nt+1):
            for j in range(1, nk[i]+1):
                print(f'K({i},{j}): {model[K[i][j]]}')
        ###############

        # TODO: Print output

    else:
        print("Unsatisfiable: error.")


if __name__ == '__main__':
    read_input()
    solve()
