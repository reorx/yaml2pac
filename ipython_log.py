
import subprocess
from subprocess import PIPE, STDOUT

f = "function add(n) {return n + 1;};"

# http://unix.stackexchange.com/questions/25372/turn-off-buffering-in-pipe
node = subprocess.Popen(
    #['node'],
    ['script', '-q', '/dev/null', 'node'],
    #['script', '-q', '/dev/null', 'python'],
    #['python', 'test_out.py'],
    #['python', '-u'],
    stdin=PIPE, stdout=PIPE, stderr=STDOUT, bufsize=0)

print 'write'
node.stdin.write('console.log("hello");' + '\n')
#node.stdin.write(f + '\n')
#node.stdin.write('print "hello"' + '\n')
#node.stdin.flush()

#node.stdout.readline()

print 'read'
node.stdout.flush()
print 'read 1'
print repr(node.stdout.read(102))
print 'read 2'
print repr(node.stdout.read(100))
#print dir(node.stdout)
print repr(node.stdout.readline().rstrip())
print repr(node.stdout.readline())
print repr(node.stdout.readline())
print repr(node.stdout.readline())
print repr(node.stdout.readline())
#for line in iter(node.stdout.readline, b''):
#    print("| " + line.rstrip())
#    if not line.rstrip():
#        break

node.stdin.write('console.log(add(1))' + '\n')
#for line in iter(node.stdout.readline, b''):
#    print("| " + line.rstrip())
print node.stdout.readline()
print node.stdout.readline()
print node.stdout.readline()
