% Problem variables (nr of tasks, release, deadline, nr of fragments, etc)
int: nt;
int: maxfrags;
array [1..nt] of int: r;
array [1..nt] of int: p;
array [1..nt] of int: d;
array [1..nt] of int: nk;
array [1..nt,1..maxfrags] of int: pk;
array [1..nt,1..nt] of int: deps;

% CSP Variables
array [1..nt] of var bool: T;
array [1..nt,1..maxfrags] of var int: K;



% Constraints

constraint forall(i in 1..nt) (T[i] = true);

%constraint forall(i in 1..nt) (
%             forall(j in 1..nk[i]) (
%               (K[i,j] >= r[i] /\ K[i,j] < d[i] - pk[i,j]) \/ K[i,j] = -1));
               



solve satisfy;

output[show(T)];
