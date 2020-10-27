import fileinput as fi

n = 0

# Initiliaze (TODO nasty -1)
r = [-1]
p = [-1]
d = [-1]
nk = [-1]
k = [[]]
deps = [[]]

# Clauses
hardclauses = []
softclauses = []

for line in fi.input():
    if fi.isfirstline():
        n = int(line)
    # TODO talvez tirar ifs
    elif fi.filelineno() <= n+1:
        line = line.split()
        r.append(int(line[0]))
        p.append(int(line[1]))
        d.append(int(line[2]))
        nk.append(int(line[3]))
        k.append([int(k) for k in line[4:]])
    else:
        line = line.split()
        if line[0] == 0:
            deps.append([])
        else:
            deps.append([int(dep) for dep in line[1:]])


# HARD CLAUSES

# SOFT CLAUSES
for task in range(1,n+1):
    softclauses.append([task])

