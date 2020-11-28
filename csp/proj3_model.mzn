% Problem variables (nr of tasks, release, deadline, nr of fragments, etc)
int: nt;
array [1..nt] of int: r;
array [1..nt] of int: p;
array [1..nt] of int: d;
array [1..nt] of int: nk;


solve satisfy;

output[show(r)]