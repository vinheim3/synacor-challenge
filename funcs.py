#returns the decimal equivalent of a hex number, any case allowed
def h2d(n):
    n=n.upper()
    total=0
    for i in range(len(n)):
        cL=n[-(i+1)]
        if cL.isdigit():
            cN=int(cL)
        else:
            cN=ord(cL)-ord('A')+10
        total+=cN*16**i
    return total

#returns a 2-digit-length uppercase hex equivalent of a 8-bit decimal number
def d2h(n):
    num=[]
    if n==0:
        return "00"
    while n!=0:
        let=n%16
        if let<10:
            num.append(str(let))
        else:
            num.append(chr(ord('A')+let-10))
        n/=16
    if len(num)==1:
        num.append("0")
    num.reverse()
    return "".join(num)

#takes low-byte(as char) and high-byte(as char) and returns the decimal
def lE(a,b):
    return h2d(d2h(ord(b))+d2h(ord(a)))
