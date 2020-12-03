# Single Machine Scheduling - Project 3

For the 3nd ALC project we developed a software tool for solving the Single Machine Scheduling (JFS) problem using CSP. We used Minizinc to model the constraints and ran the default solver (Gecode 6.3.0).


## Implementation

We defined the following variables:

* #### *T(i)*: task *i* is completed
* #### *K(i,j)*: timestamp in which fragment *j* of task *i* starts its execution


The following constraints were used to encode the problem:

* Task's "flags" can only be assigned to 0 or 1
  > And(T[i] >= 0, T[i] <= 1)

* Force all fragments of non executed tasks to have a fixed arbitrary value (in this case, r[i])
  > Or(T[i] == 1, And([K[i][j] == r[i] for j in range(1, nk[i])]))

* Fragments can only be executing between their task's release and deadline
  > Or(T[i] == 0, And(K[i][j] >= r[i], K[i][j] + pk[i][j] <= d[i]))

* Fragments must be processed in order
  > Or(T[i] == 0, K[i][j-1] + pk[i][j-1] <= K[i][j])

* Only one fragment can be executing at a time
  > Or(Or(T[i1]==0, T[i2]==0), If(K[i1][j1] > K[i2][j2], K[i1][j1] >= K[i2][j2] + pk[i2][j2], K[i2][j2] >= K[i1][j1] + pk[i1][j1]))

* Task can only start if all its dependencies are done
  > If(T[dep] == 1, Or(T[i] == 0,  K[i][1] >= K[dep][nk[dep]] + pk[dep][nk[dep]]), T[i] == 0)


## Installation

To install Z3-Solver:

```bash
pip3 install z3-solver
```

## Requirements

* Python 3 or above


## Usage

```bash
python proj2.py < job.sms > solution.txt
```
Use python3 if your default is python2.


## Contributors

* João Palet
* Miguel Grilo
