# Single Machine Scheduling - Project 1

For the 1st ALC project we developed a software tool for solving the Single Machine Scheduling (JFS) problem using MaxSAT. The solver we used was [Open-WBO](http://sat.inesc-id.pt/open-wbo/).


## Implementation

We defined the following variables:

* T(i): task i is completed
* K(i,j,t): fragment j of task i is being executed in timestep t

In order to map these variables (encoded as tuples) to WCNF literals we used two Python dictionaries.

The following constraints were used to encode the problem:

> Hard Clauses

* A fragment of a task can only be processed during the processing interval of its task (after the release and before the deadline). 


## Installation

To install Open-WBO:

```bash
cd solvers
make
```

## Requirements

* Python 3.7 or above


## Usage

```bash
python proj1.py < job.sms > solution.txt
```
Use python3 (or python3.7) if your default is python2.


## Contributors

* João Palet
* Miguel Grilo