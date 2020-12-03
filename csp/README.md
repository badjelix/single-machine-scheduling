# Single Machine Scheduling - Project 3

For the 3nd ALC project we developed a software tool for solving the Single Machine Scheduling (JFS) problem using CSP. We used Minizinc to model the constraints and ran the default solver (Gecode 6.3.0).


## Implementation

We defined the following variables:

* #### *T(i)* (bool): task *i* is completed
* #### *K(i,j)* (int): timestamp in which fragment *j* of task *i* starts its execution


The following constraints were used to encode the problem:

* Force all fragments of non executed tasks to have a fixed arbitrary value (in this case, r[i])
  > T[i] = false -> K[i,j] = r[i]

* Fragments can only be executing between their task's release and deadline
  > K[i,j] >= r[i] /\ K[i,j] <= d[i] - pk[i,j]

* Fragments must be processed in order
  > T[i] = true -> K[i,j-1] + pk[i,j-1] <= K[i,j]
  
* Only one fragment can be executing at a time
  > K[i,j] >= K[bi, bj] + pk[bi, bj] \/ K[bi, bj] >= K[i,j] + pk[i,j] \/ T[i] = false \/ T[bi] = false

* Task can only start if all its dependencies are done
  > if T[dep] = true then T[i] = false \/ K[i,1] >= K[dep,nk[dep]] + pk[dep,nk[dep]] else T[i] = false endif


## Installation

To install Minizinc:

[https://www.minizinc.org/doc-2.4.3/en/installation.html](https://www.minizinc.org/doc-2.4.3/en/installation.html)

## Requirements

* Python 3 or above


## Usage

```bash
python proj3.py < job.sms > solution.txt
```
Use python3 if your default is python2.


## Contributors

* João Palet
* Miguel Grilo
