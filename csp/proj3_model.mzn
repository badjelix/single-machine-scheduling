include "alldifferent_except_neg1.mzn";

% PROBLEM CONSTANTS

int: nt;
int: maxdeadline;
int: maxfrags;
array [1..nt] of int: r;
array [1..nt] of int: p;
array [1..nt] of int: d;
array [1..nt] of int: nk;
array [1..nt,1..maxfrags] of int: pk;
array [1..nt] of set of 1..nt: deps;



% CSP VARIABLES

array [1..nt] of var bool: T;
array [1..nt,1..maxfrags] of var -1..maxdeadline: K;



% CONSTRAINTS

% Fragments can only be executing between their task’s release and deadline
constraint forall(i in 1..nt) (
             forall(j in 1..nk[i]) (
               (K[i,j] >= r[i] /\ K[i,j] <= d[i] - pk[i,j]) \/ K[i,j] = -1
             )
           );
           
% Fragments that are not relevant but must exist because we can't create dynamic size arrays in Minizinc are forced to have value -1
constraint forall(i in 1..nt) (
             forall(j in nk[i]+1..maxfrags) (
               K[i,j] = -1
             )
           );
           
% Fragments must be processed and in order
constraint forall(i in 1..nt) (
             forall(j in 2..nk[i]) (
               (T[i] = true) -> K[i,j-1] + pk[i,j-1] <= K[i,j]
             /*forall(j in 1..nk[i]-1) (
               if K[i,j] != -1 then K[i,j] + pk[i,j] <= K[i,j+1] else K[i,j+1] = -1 endif*/
             )
           );
           
% Task is completed if its last fragment is executed
constraint forall(i in 1..nt) (if K[i,1] >= 0 then T[i] = true else T[i] = false endif);
           
% Only one fragment can be executing at a time - FIXME
% constraint alldifferent_except_neg1([K[i,j] | i in 1..nt, j in 1..maxfrags]);

% Only one fragment can be executing at a time (VERSAO SMT)
constraint forall(i in 1..nt) (
             forall(j in 1..nk[i]) (
               forall(bi in i+1..nt) (
                 forall(bj in 1..nk[bi]) (
                   K[i,j] >= K[bi, bj] + pk[bi, bj] \/ K[bi, bj] >= K[i,j] + pk[i,j] \/ bool2int(T[i]) + bool2int(T[bi]) < 2
                 )
               )
             )
          );

% Task can only start if all its dependencies are done
constraint forall(i in 1..nt) (
             forall(dep in deps[i]) (
               if T[dep] = true then
                                  T[i] = false \/ K[i,1] >= K[dep,nk[dep]] + pk[dep,nk[dep]]
                                else
                                  T[i] = false
               endif
               /*T[i] = false \/ (T[dep] = true /\ K[i,1] >= K[dep,nk[dep]] + pk[dep,nk[dep]])*/
             )
           );

               


% SOLVE

solve maximize sum(i in 1..nt) (bool2int(T[i]));

output[show(T) ++ "|"];
output[show(K)];
