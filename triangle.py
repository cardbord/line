from time import sleep
size = int(input("size?"))

a = []
for _ in range(size):
    a.append('-')
    
a[size//2] = '*'
b = []
for _ in range(size):
    b.append('-')

print(''.join([_ for _ in a]))

#here so far...

while 1:
    for x in range(0,size-3):
        c = a[x:x+3]
        
        d = c[0]
        dd = x
        e = c[1]
        ee = x+1
        f = c[2]
        ff = x+2
        if d != f:
            if e == '-':
                b[ee] = '*'

                
        
    print(''.join([_ for _ in b]))
    sleep(0.1)
        
    a = []
    for _ in range(size):
        a.append('-')  
        
        
    for x in range(0,size-3):
        c = b[x:x+3]
        d = c[0]
        dd = x
        e = c[1]
        ee = x+1
        f = c[2]
        ff = x+2
        if d != f:
            if e == '-':
                a[ee] = '*'
                
    
    print(''.join([_ for _ in a]))
    sleep(0.1)
        
    b = []
    for _ in range(size):
        b.append('-')