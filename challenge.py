#funcs contains lE, which returns the decimal equivalent of a
#little-endian pair given the low-byte and high-byte as 2 chars
import sys,funcs

data=open("challenge.bin","rb").read()
register=[0,0,0,0,0,0,0,0] #registers referenced through 32768-32775
callStack=[] #stack of insI to pop and Ret to
insI=0 #instructionIndex, also known as pc

#adds is the array of little-endian 16-bit pairs as integers
adds = list(funcs.lE(data[i],data[i+1]) for i in range(0,len(data)-1,2))

#shorthand to reference correct register addresses
def r(x): return x-32768

#returns either x or the value in the register x
def get(x):
    if 0<=x<=32767:
        return x
    elif 32768<=x<=32775:
        return register[r(x)]
    else:
        print "Invalid access for getting"
        sys.exit()

#sets x to a value, or sets the register x to a value
def sets(x,y):
    if 0<=x<=32767:
        adds[x]=get(y)
    elif 32768<=x<=32775:
        register[r(x)]=get(y)
    else:
        print "Invalid access for setting"
        sys.exit()

#can also be called if executing Ret, but have an empty call stack
def Halt():
    print "Program terminated"
    sys.exit()

#a set function for registers only
def Set  (x,y  ) : register[r(x)] = get(y)

#push onto call stack without having to call from it
def Push (x    ) : callStack.append(get(x))

#remove an item from call stack without having to Ret to it
def Pop  (x    ) : sets(x, callStack.pop())

#x is 1 if y and z are equal, and 0 otherwise
def Eq   (x,y,z) : sets(x, int(get(y)==get(z)))

#x is 1 if y is greater than z, and 0 otherwise
def Gt   (x,y,z) : sets(x, int(get(y)> get(z)))

#start executing from a different position
def Jmp  (x    ) : return get(x)

#Jump to y if x is non-zero
def Jt(x,y):
    if get(x)!=0:
        return Jmp(y)

#Jump to y if x is zero
def Jf(x,y):
    if get(x)==0:
        return Jmp(y)

#bitwise operations
def Add  (x,y,z) : sets(x,(get(y) + get(z))%32768)
def Mult (x,y,z) : sets(x,(get(y) * get(z))%32768)
def Mod  (x,y,z) : sets(x, get(y) % get(z))
def And  (x,y,z) : sets(x, get(y) & get(z))
def Or   (x,y,z) : sets(x, get(y) | get(z))
def Not  (x,y  ) : sets(x, 32767  - get(y))

#set x to the value in the memory address y
def Rmem (x,y  ) : sets(x,adds[get(y)])

#set the memory or register address x to y
def Wmem (x,y  ) : sets(get(x),get(y))

#call a function, and set the opcode after as the point to return to
def Call(x):
    global insI
    callStack.append(insI+2)
    return Jmp(get(x))

#return to the memory address given at the top of the stack
def Ret():
    if callStack==[]:
        Halt()
    else:
        return Jmp(callStack.pop())

#print the ascii code of x
def Out(x): sys.stdout.write(chr(get(x)))

#read in a character at a time and store it in x
def In(x):
    try:
        char = sys.stdin.read(1)
    except IOError:
        char = sys.stdin.read(1)
    sets(x,ord(char))

#virtually a pass that also increments insI or pc
def Noop(): pass

#1.opcodes can be called like a function, based on the opcode given
#2.they return None if the main loop will set the next instruction based on
#  the chosen functions arguments, or an index set by a jump function
opcodes = {
    0  : [Halt, 0],
    1  : [Set,  2],
    2  : [Push, 1],
    3  : [Pop,  1],
    4  : [Eq,   3],
    5  : [Gt,   3],
    6  : [Jmp,  1],
    7  : [Jt,   2],
    8  : [Jf,   2],
    9  : [Add,  3],
    10 : [Mult, 3],
    11 : [Mod,  3],
    12 : [And,  3],
    13 : [Or,   3],
    14 : [Not,  2],
    15 : [Rmem, 2],
    16 : [Wmem, 2],
    17 : [Call, 1],
    18 : [Ret,  0],
    19 : [Out,  1],
    20 : [In,   1],
    21 : [Noop, 0]
}

#process opcodes 1 at a time, giving them the right number of arguments
while 0<=insI<len(adds):
    args=list(adds[insI+1+i] for i in range(opcodes[adds[insI]][1]))
    a=opcodes[adds[insI]][0](*args)
    insI=insI+len(args)+1 if a==None else a

#insI (or pc) should never reference a value outside of the bin file
print "Error. Memory address referenced is out of bounds"
