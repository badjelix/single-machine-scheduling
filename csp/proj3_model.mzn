include "alldifferent_except_neg1.mzn";



% PROBLEM CONSTANTS

int: nt;
int: maxfrags;
int: maxdeps;
array [1..nt] of int: r;
array [1..nt] of int: p;
array [1..nt] of int: d;
array [1..nt] of int: nk;
array [1..nt,1..maxfrags] of int: pk;
array [1..nt,1..maxdeps] of int: deps;



% CSP VARIABLES

array [1..nt] of var bool: T;
array [1..nt,1..maxfrags] of var int: K;



% CONSTRAINTS

% Fragments can only be executing between their task’s release and deadline
constraint forall(i in 1..nt) (
             forall(j in 1..nk[i]) (
               (K[i,j] >= r[i] /\ K[i,j] < d[i] - pk[i,j]) %\/ K[i,j] = -1
             )
           );
constraint forall(i in 1..nt) (
             forall(j in nk[i]+1..maxfrags) (
               K[i,j] = -1
             )
           );
           
% Only one fragment can be executing at a time - FIXME
constraint alldifferent_except_neg1([K[i,j] | i in 1..nt, j in 1..maxfrags]);
               


% SOLVE

solve maximize sum(i in 1..nt) (bool2int(T[i]));

%output[show(T)];
