#returns the decimal equivalent of a hex number, any case allowed
def h2d(n):
    n=n.upper()[::-1]
    total=0
    for i in range(len(n)):
        cL=n[i]
        total+=(int(cL) if cL.isdigit() else ord(cL)-ord('A')+10)*16**i
    return total

#returns a 2-digit-length uppercase hex equivalent of a 8-bit decimal number
def d2h(n):
    a=hex(n).upper()[2::]
    return "0"+a if len(a)==1 else a

#takes low-byte(as char) and high-byte(as char) and returns the decimal
def lE(a,b): return h2d(d2h(ord(b))+d2h(ord(a)))
