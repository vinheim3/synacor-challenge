from funcs import lE
import sys

data=open("challenge.bin","rb").read()
register=[0,0,0,0,0,0,0,0]
callStack=[]
insI=0

#adds is the array of little-endian pairs as integers to know where to return from jumps
adds=[]
for i in range(0,len(data)-1,2):
    adds.append(lE(data[i],data[i+1]))

def r(x): return x-32768

def get(x):
    global register
    if 0<=x<=32767:
        return x
    elif 32768<=x<=32775:
        return register[r(x)]
    else:
        print "Invalid access"

def sets(x,y):
    global adds,register
    if 0<=x<=32767:
        adds[x]=get(y)
    elif 32768<=x<=32775:
        register[r(x)]=get(y)
    else:
        print "Invalid access"

def Halt():
    print "Program terminated"
    sys.exit()

def Set  (x,y  ) : global insI,register; register[r(x)]=get(y); insI+=3

def Push (x    ) : global insI,callStack; callStack.append(get(x)); insI+=2

def Pop  (x    ) : global insI,callStack; sets(x, callStack.pop()); insI+=2

def Eq   (x,y,z) : global insI; sets(x, int(get(y) == get(z))); insI+=4

def Gt   (x,y,z) : global insI; sets(x, int(get(y) >  get(z))); insI+=4

def Jmp  (x    ) : global insI; insI=get(x)

def Jt(x,y):
    global insI
    if get(x)!=0:
        Jmp(y)
    else:
        insI+=3

def Jf(x,y):
    global insI
    if get(x)==0:
        Jmp(y)
    else:
        insI+=3

def Add  (x,y,z) : global insI; sets(x, (get(y) + get(z))%32768); insI+=4

def Mult (x,y,z) : global insI; sets(x, (get(y) * get(z))%32768); insI+=4

def Mod  (x,y,z) : global insI; sets(x,  get(y) % get(z)); insI+=4

def And  (x,y,z) : global insI; sets(x,  get(y) & get(z)); insI+=4

def Or   (x,y,z) : global insI; sets(x,  get(y) | get(z)); insI+=4

def Not  (x,y  ) : global insI; sets(x,  32767  - get(y)); insI+=3

def Rmem (x,y  ) : global insI,adds; sets(x,adds[get(y)]); insI+=3

def Wmem (x,y  ) : global insI;      sets(get(x),get(y)); insI+=3

def Call(x):
    global callStack,insI
    callStack.append(insI+2)
    Jmp(get(x))

def Ret():
    global callStack
    if callStack==[]:
        Halt()
    else:
        Jmp(callStack.pop())

def Out(x):
    global insI
    sys.stdout.write(chr(get(x)))
    insI+=2

def In(x):
    global insI
    try:
        char = sys.stdin.read(1)
    except IOError:
        char = sys.stdin.read(1)
    sets(x,ord(char))
    insI+=2

def Noop():
    global insI
    insI+=1

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

#process instructions
while insI<len(adds):
    #print str(insI)+": "+str(adds[insI])
    if adds[insI] in (0,18,21):
        opcodes[adds[insI]]()
    elif adds[insI] in (2,3,6,17,19,20):
        opcodes[adds[insI]](adds[insI+1])
    elif adds[insI] in (1,7,8,14,15,16):
        opcodes[adds[insI]](adds[insI+1],adds[insI+2])
    elif adds[insI] in (4,5,9,10,11,12,13):
        opcodes[adds[insI]](adds[insI+1],adds[insI+2],adds[insI+3])