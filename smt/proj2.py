import fileinput as fi
from z3 import Solver
from z3 import Bool, Int, sat, IntVal, Or, And, If, Distinct, Optimize, Implies, Sum


# HACK we initialized the 0th entry of each array so we could reference tasks by their number according the problem specification
# e.g. task 1 release time can be accessed with r[1]

nt = 0          # number of tasks
r = [-1]        # release time of each task
p = [-1]        # total processing time of tasks
d = [-1]        # deadline time of each task
nk = [-1]       # number of fragments of each task
pk = [[]]       # processing time of each fragment of each task
deps = [[]]     # dependencies of each task


def read_input():
    global nt, r, p, d, nk, pk, deps

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


    # Task's "flags" can only be assigned to 0 or 1
    for i in range(1, nt+1):
        solver.add(And(T[i] >= 0, T[i] <= 1))

    
    # Force all fragments of non executed tasks to a given value
    for i in range(1, nt+1):
        solver.add(Or(T[i] == 1, And([K[i][j] == r[i] for j in range(1, nk[i])])))


    # Fragments can only be executing between their task's release and deadline
    for i in range(1, nt+1):
        for j in range(1, nk[i]+1):
            solver.add(Or(T[i] == 0, And(K[i][j] >= r[i], K[i][j] + pk[i][j] <= d[i])))

    
    # Fragments must be processed in order
    for i in range(1, nt+1):
        for j in range(2, nk[i]+1): # All except the first one
            solver.add(Or(T[i] == 0, K[i][j-1] + pk[i][j-1] <= K[i][j]))

    
    # Only one fragment can be executing at a time
    for i in range(1, nt+1):
        for j in range(1, nk[i]+1):
            for bi in range(i, nt+1):
                for bj in range(1, nk[bi]+1):
                    if not (i == bi and j == bj):
                        solver.add(Or( Or(T[i]==0, T[bi]==0), If(K[i][j] > K[bi][bj], K[i][j] >= K[bi][bj] + pk[bi][bj], K[bi][bj] >= K[i][j] + pk[i][j])))


    # Task can only start if all its dependencies are done
    for i in range(1, nt+1):
        for dep in deps[i]:
            solver.add(If(T[dep] == 1, Or(T[i] == 0,  K[i][1] >= K[dep][nk[dep]] + pk[dep][nk[dep]]), T[i] == 0))

    solver.maximize(Sum([t for t in T]))

    if solver.check() == sat:
        model = solver.model()

        output = ''

        # Print optimum number of processed tasks
        optimal = 0
        for i in range(1, nt+1):
            if model[T[i]] == 1:
                optimal += 1
        output += str(optimal)

        # For every task that is processed, print its fragments
        for i in range(1, nt+1):
            taskinfo = ''
            if model[T[i]] == 1:
                taskinfo += '\n' + str(i)
                for j in range(1, nk[i]+1):
                    taskinfo += ' ' + str(model[K[i][j]])
                output += taskinfo
        
        print(output)

    else:
        print("Unsatisfiable: error.")


if __name__ == '__main__':
    read_input()
    solve()
