from funcs import lE
import sys

data=open("challenge.bin","rb").read()
register=[0,0,0,0,0,0,0,0]
callStack=[] #stack of insI to Ret to after a Call
insI=0 #instructionIndex, also known as pc

#adds is the array of little-endian 16-bit pairs as integers
adds=[]
for i in range(0,len(data)-1,2):
    adds.append(lE(data[i],data[i+1]))

#shorthand to reference correct register addresses
def r(x): return x-32768

#returns either x or the value in the register x
def get(x):
    if 0<=x<=32767:
        return x
    elif 32768<=x<=32775:
        return register[r(x)]
    else:
        print "Invalid access"

#sets x to a value, or sets the register x to a value
def sets(x,y):
    if 0<=x<=32767:
        adds[x]=get(y)
    elif 32768<=x<=32775:
        register[r(x)]=get(y)
    else:
        print "Invalid access"

#can also be called if executing Ret, but have an empty call stack
def Halt (     ) : print "Program terminated"; sys.exit()

#a set function for registers only
def Set  (x,y  ) : global insI; register[r(x)] = get(y);      insI+=3

#push onto call stack without having to call from it
def Push (x    ) : global insI; callStack.append(get(x));     insI+=2

#remove an item from call stack without having to Ret to it
def Pop  (x    ) : global insI; sets(x, callStack.pop()    ); insI+=2

#x is 1 if y and z are equal, and 0 otherwise
def Eq   (x,y,z) : global insI; sets(x, int(get(y)==get(z))); insI+=4

#x is 1 if y is greater than z, and 0 otherwise
def Gt   (x,y,z) : global insI; sets(x, int(get(y)> get(z))); insI+=4

#start executing from a different position
def Jmp  (x    ) : global insI; insI=get(x)

#Jump to y if x is non-zero
def Jt(x,y):
    global insI
    if get(x)!=0:
        Jmp(y)
    else:
        insI+=3

#Jump to y if x is zero
def Jf(x,y):
    global insI
    if get(x)==0:
        Jmp(y)
    else:
        insI+=3

#bitwise operations
def Add  (x,y,z) : global insI; sets(x,(get(y) + get(z))%32768); insI+=4
def Mult (x,y,z) : global insI; sets(x,(get(y) * get(z))%32768); insI+=4
def Mod  (x,y,z) : global insI; sets(x, get(y) % get(z));        insI+=4
def And  (x,y,z) : global insI; sets(x, get(y) & get(z));        insI+=4
def Or   (x,y,z) : global insI; sets(x, get(y) | get(z));        insI+=4
def Not  (x,y  ) : global insI; sets(x, 32767  - get(y));        insI+=3

#set x to the value in the memory address y
def Rmem (x,y  ) : global insI; sets(x,adds[get(y)]); insI+=3

#set the memory or register address x to y
def Wmem (x,y  ) : global insI; sets(get(x),get(y)); insI+=3

#call a function, and set the opcode after as the point to return to
def Call (x    ) : global insI; callStack.append(insI+2); Jmp(get(x))

#return to the memory address given at the top of the stack
def Ret  (     ) : Halt() if callStack==[] else Jmp(callStack.pop())

#print the ascii code of x
def Out  (x    ) : global insI; sys.stdout.write(chr(get(x)));insI+=2

#read in a character at a time and store it in x
def In(x):
    global insI
    try:
        char = sys.stdin.read(1)
    except IOError:
        char = sys.stdin.read(1)
    sets(x,ord(char))
    insI+=2

#virtually a pass that also increments insI or pc
def Noop(): global insI; insI+=1

#opcodes can be called like a function, based on the opcode given
opcodes = {
    0  : lambda       : Halt (     ),
    1  : lambda x,y   : Set  (x,y  ),
    2  : lambda x     : Push (x    ),
    3  : lambda x     : Pop  (x    ),
    4  : lambda x,y,z : Eq   (x,y,z),
    5  : lambda x,y,z : Gt   (x,y,z),
    6  : lambda x     : Jmp  (x    ),
    7  : lambda x,y   : Jt   (x,y  ),
    8  : lambda x,y   : Jf   (x,y  ),
    9  : lambda x,y,z : Add  (x,y,z),
    10 : lambda x,y,z : Mult (x,y,z),
    11 : lambda x,y,z : Mod  (x,y,z),
    12 : lambda x,y,z : And  (x,y,z),
    13 : lambda x,y,z : Or   (x,y,z),
    14 : lambda x,y   : Not  (x,y  ),
    15 : lambda x,y   : Rmem (x,y  ),
    16 : lambda x,y   : Wmem (x,y  ),
    17 : lambda x     : Call (x    ),
    18 : lambda       : Ret  (     ),
    19 : lambda x     : Out  (x    ),
    20 : lambda x     : In   (x    ),
    21 : lambda       : Noop (     )
}

#process opcodes 1 at a time, giving them the right number of arguments
while 0<=insI<len(adds):
    if adds[insI] in (0,18,21):
        opcodes[adds[insI]]()
    elif adds[insI] in (2,3,6,17,19,20):
        opcodes[adds[insI]](adds[insI+1])
    elif adds[insI] in (1,7,8,14,15,16):
        opcodes[adds[insI]](adds[insI+1],adds[insI+2])
    elif adds[insI] in (4,5,9,10,11,12,13):
        opcodes[adds[insI]](adds[insI+1],adds[insI+2],adds[insI+3])

#insI or pc should never reference a value outside of the bin file
print "Error. Memory address referenced is out of bounds"
