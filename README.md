# Single Machine Scheduling - Project 1

For the 1st ALC project we developed a software tool for solving the Single Machine Scheduling (JFS) problem using MaxSAT. The solver we used was [Open-WBO](http://sat.inesc-id.pt/open-wbo/).


## Implementation

We defined the following variables:

* *T(i)*: task *i* is completed
* *K(i,j,t)*: fragment *j* of task *i* is being executed in timestep *t*

In order to map these variables (encoded as tuples) to WCNF literals we used two Python dictionaries.

The following constraints were used to encode the problem:

> Hard Clauses

* A fragment of a task can only be processed during the processing interval of its task. In that way, a variable *K(i,j,t)* will only exist when *t* has a value between the task's release and deadline.

* Fragments must be processed in order.

* If a fragment *j* of task *i* starts its execution at a given timestep *t*, it will be executed until it is completed and won't be executed any more after that (*K(i, j, x)* will be 1 for every *t <= x < t + processing_time(i, j)* and will be 0 from then on).

* Only one fragment can be executing at any timestep t. This was encoded as a cardinality constraint using bitwise encoding.

* A task is completed if its last fragment is completed.

* A task can only start processing if all of its dependencies are already completed.

> Soft Clauses

* Execute as many tasks *i* as possible (*T(i)* for every task *i*).


## Installation

To install Open-WBO:

```bash
cd solvers/wbo

make
```

## Requirements

* Python 3 or above


## Usage

```bash
python proj1.py < job.sms > solution.txt
```
Use python3 if your default is python2.


## Contributors

* João Palet
* Miguel Grilo
