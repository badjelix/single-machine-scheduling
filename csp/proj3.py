import subprocess


# HACK we initialized the 0th entry of each array so we could reference tasks by their number according the problem specification
# e.g. task 1 release time can be accessed with r[1]

nt = 0          # number of tasks
r = [-1]        # release time of each task
p = [-1]        # total processing time of tasks
d = [-1]        # deadline time of each task
nk = [-1]       # number of fragments of each task
pk = [[]]       # processing time of each fragment of each task
deps = [[]]     # dependencies of each task


def read_input():
    global nt, r, p, d, nk, pk, deps

    # Get data from .sms file
    for line in fi.input():
        if fi.isfirstline():
            nt = int(line)
        elif fi.filelineno() <= nt+1:
            line = line.split()
            r.append(int(line[0]))
            p.append(int(line[1]))
            d.append(int(line[2]))
            nk.append(int(line[3]))
            pk.append([-1] + [int(k) for k in line[4:]])
        else:
            line = line.split()
            if line[0] == 0:
                deps.append([])
            else:
                deps.append([int(dep) for dep in line[1:]])


def build_data():
    
    data = ''
    data += 'nt = ' str(nt) + '\n'
    data += '['

    return data


def solve():
    # TODO chamar subprocesso com o .mzn e passar como argumento o .dzn

    pass


if __name__ == '__main__':
    read_input()
    data = build_data()
    solve()



'''data = "value = 300;" \
        "x = 5;" \
        "y = 10;"
ps = subprocess.Popen(('minizinc', 'model.mzn', '-'),
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        encoding='utf-8')
output, _ = ps.communicate(data)
output = output.split('\n')
print(output)'''