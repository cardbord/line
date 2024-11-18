import sys

a = sys.argv

def conv_c(num:int):
    _temp = str(bin(int(num)))
    b = '0'+_temp.replace('0b','')
    b=b.replace('0','/')
    b=b.replace('1','\\')
    print(b)
    

for i in a:
    if i.isnumeric():
        conv_c(i)        