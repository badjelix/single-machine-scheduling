% PROBLEM CONSTANTS

int: nt;
int: maxfrags;
array [1..nt] of int: r;
array [1..nt] of int: p;
array [1..nt] of int: d;
array [1..nt] of int: nk;
array [1..nt,1..maxfrags] of int: pk;
array [1..nt,1..nt] of int: deps;


% CSP VARIABLES

array [1..nt] of var bool: T;
array [1..nt,1..maxfrags] of var int: K;



% CONSTRAINTS

% Dummy 
constraint forall(i in 1..nt) (T[i] = true);

% Fragments can only be executing between their task’s release and deadline
constraint forall(i in 1..nt) (
             forall(j in 1..nk[i]) (
               (K[i,j] >= r[i] /\ K[i,j] < d[i] - pk[i,j]) \/ K[i,j] = -1));
               


% SOLVE

solve satisfy;

output[show(T)];
