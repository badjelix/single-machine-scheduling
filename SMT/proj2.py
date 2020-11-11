from z3 import Solver
from z3 import Bool, Int, sat, IntVal
from z3 import Or, And, If, Distinct


# define variables


def read_input():
    pass


def solve(puzzle):
    solver = Solver()

    if solver.check() == sat:
        model = solver.model()
        # print model

    else:
        print("Unsatisfiable: error.")


if __name__ == '__main__':
    read_input()
    solve()
