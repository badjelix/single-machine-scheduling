import time
import subprocess
 
if __name__ == '__main__':
    data = "value = 300;" \
           "x = 5;" \
           "y = 10;"
    ps = subprocess.Popen(('minizinc', 'model.mzn', '-'),
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          encoding='utf-8')
    output, _ = ps.communicate(data)
    output = output.split('\n')
    print(output)