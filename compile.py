f = 'test.ln'
#f = input("Enter filename")
d=[]

memory = {}

global acc
acc = 0

def bin_to_int(binary:str):
    temp=0
    for c in range(len(binary)-1,-1, -1):
        if binary[c] == '1':
            temp+= 2**(len(binary)-1-c) if c != 0 else -(2**(len(binary)-1-c))
    return temp


def between(line:str,char):
    char1 = line.find(char)
    if char1==-1:
        return ''

    return line[char1+1:line.find(char,char1+1)]


with open(f,'r') as a:
    d=a.readlines()

l=0
while l < len(d):
    
    line = d[l]
    line.strip()
    
    line.replace(' ','')
    
    
    
    opcode = between(line,'_')
    operand = between(line,'=')
    condition = between(line,'|')
    
    condition_opc = between(condition,"'")
    condition_oper = between(condition,"=")
    
    condition_oper = list(condition_oper)
    if condition_oper!='':
        for char in range(len((condition_oper))):
            if condition_oper[char] == '/':
                condition_oper[char] = '0'
            elif condition_oper[char] == "\\":
                condition_oper[char] = '1'
        
        condition_oper = ''.join(condition_oper)
    
    
    
    operand = list(operand)
    if operand!='':
        for char in range(len((operand))):
            if operand[char] == '/':
                operand[char] = '0'
            elif operand[char] == "\\":
                operand[char] = '1'
        
        operand = ''.join(operand)
        
        num = bin_to_int(operand)
    
    cond = True
    match condition_opc:
        case '/': #brz
            cond = (acc == 0)
        case '\\': #brp
            cond = (acc > 0)
        case '¬/': #neg brz
            cond = not (acc == 0)
        case '¬\\': #neg brp
            cond = not (acc > 0)
        case '>/':
            cnum = bin_to_int(condition_oper)
            cond = (acc >= cnum)
        case '\\<':
            cnum = bin_to_int(condition_oper)
            cond = (acc <= cnum)
        case '---':
            cnum = bin_to_int(condition_oper)
            cond = (acc==cnum)
            
    
    
    if cond:
        match opcode:
            case '--': #add
                acc+=num
            case '-': #sub
                acc-=num
            case '<<': #out
                print(operand)
                if operand=='':
                    print(acc,end='',sep='')
                else:
                    print(chr(num),end='',sep='')
            case '<>': #newline
                print('',end='\n',sep='')
                
            case '<': #sta
                memory[num]=acc
            case '>': #lda
                acc=memory[num]
            case '->': #goto
                l=num-1
                
            
            
    l+=1                

                