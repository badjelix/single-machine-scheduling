import fileinput as fi
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
maxfrags = 0


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
    global maxfrags
    
    data = ''

    # nt
    data += 'nt = ' + str(nt) + ';\n'

    # r
    data += 'r = ['
    for i in range(1,len(r)):
        data += str(r[i]) + ','
    data += '];\n'
    
    # p
    data += 'p = ['
    for i in range(1,len(p)):
        data += str(p[i]) + ','
    data += '];\n'

    # d
    data += 'maxdeadline = ' + str(max(d)) + ';\n'
    data += 'd = ['
    for i in range(1,len(d)):
        data += str(d[i]) + ','
    data += '];\n'

    # nk
    data += 'nk = ['
    for i in range(1,len(nk)):
        data += str(nk[i]) + ','
    data += '];\n'

    # pk
    maxfrags = max(nk)
    data += 'maxfrags = ' + str(maxfrags) + ';\n'
    data += 'pk = ['
    for i in range(1, len(pk)):
        data += '|'
        for j in range(1, maxfrags+1):
            if j < len(pk[i]):
                data += str(pk[i][j]) + ','
            else:
                data += '-1,'
    data += '|];\n'

    # deps
    maxdeps = len(max(deps))
    data += 'deps = ['   
    for i in range(1, len(deps)):
        data += '{'
        for j in range(0, len(deps[i])):
            data += str(deps[i][j]) + ','
        data += '},'
    data += '];'
    # print(data)
    return data


def solve(data):
    ps = subprocess.Popen(('minizinc', 'proj3_model.mzn', '-'),
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        encoding='utf-8')
    output, _ = ps.communicate(data)
    output = output.split('\n')

    # Converting string output to solution
    solution = ''
    output = output[0].replace(" ", "").split('|')
    for i in range(len(output)):
        output[i] = output[i].strip('[]\'').split(',')
    
    n_executed = output[0].count('true')
    solution += f'{n_executed}'
    for task in range(len(output[0])):
        if output[0][task] == 'true':
            solution += f'\n{task+1}'

            index = task * maxfrags
            for frag in range(nk[task+1]):
                solution += f' {output[1][index+frag]}'

    # Print solution
    print(solution)
        

    
        


if __name__ == '__main__':
    read_input()
    data = build_data()
    solve(data)
