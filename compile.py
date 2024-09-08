import sys
import time
import os
import random
f = sys.argv[1]
debug = False
if len(sys.argv) > 2:
    debug = True
d=[]

memory = {}



opr_type = '/\\'

global acc
acc = 0
return_on_next=False

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
    
    neg_cond = False
    line = d[l]
    line.strip()
    
    line.replace(' ','')
    
    
    
    opcode = between(line,'_')
    operand = between(line,'=')
    condition = between(line,'|')
    
    condition_opc = between(condition,"'")
    condition_oper = between(condition,'"')
    
    typer= between(line,'+')
    
    
        
    
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
    if ('¬') in condition_opc:
        neg_cond = True
        
        condition_opc=condition_opc[2:]
    
    if opr_type == '>' and condition_oper!='':
        condition_oper = memory[bin_to_int(condition_oper)]
    else:
        condition_oper = bin_to_int(condition_oper)
    match condition_opc:
        case '/': #brz
            cond = (acc == 0)
        case '\\': #brp
            cond = (acc > 0)
        case '>/': #br if acc >= num
            cnum = condition_oper
            cond = (acc >= cnum)
        case '\\<': #br if acc <= num
            cnum = condition_oper
            cond = (acc <= cnum)
        case '---': #br if acc == num
            
            cnum = condition_oper
            cond = (acc==cnum)
            
    if neg_cond:
        cond = not cond
    
    if typer != '':
        opr_type = typer
        if debug:
            print(f'CONDITION CHANGED TO {opr_type}')
        
    if cond:
        
        match opcode:
            case '--': #add
                
                if opr_type=='/\\':
                    acc+=num
                elif opr_type=='>':
                    acc+=memory[num]
                    
            case '-': #sub
                if opr_type=='/\\':
                    acc-=num
                elif opr_type=='>':
                    acc-=memory[num]
                
                
            case '<<': #out
                if return_on_next:    
                    if opr_type=='/\\':
                        print('\n'+str(acc),end='',sep='')
                    elif '¬' in opr_type:
                        if num!='':
                            print('\n'+str(chr(num % 256)),end='',sep='')
                            
                    else:
                        print('\n'+str(acc),end='',sep='')
                    return_on_next=False
                else:
                    if operand=='':
                        print(acc,end='',sep='')
                    else:
                        print(chr(num % 256),end='',sep='')
                    
            case '<>': #return on next
                if return_on_next==True:
                    print('')
                return_on_next = True
                
            case '<': #sta
                memory[num]=acc
            case '>': #lda
                acc=memory[num]
            case '->': #goto
                if opr_type=='/\\':
                    l=num-1
                elif opr_type=='>':
                    l=memory[num]-1
                else:
                    l=num-1
                
            case '>>': #in
                acc = int(input(""))
                
            case '<-/->': #clearscreen
                os.system('cls')

            case '/->-/': #random
                acc = random.randrange(num)
                
            
            
            
    l+=1

    if debug:
        time.sleep(0.1)
        print(l, memory, acc, opcode, operand, condition_oper, cond, opr_type)
        print('')