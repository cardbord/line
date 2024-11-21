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
try:
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
                                print('\n'+str(chr(memory[acc] % 256)),end='',sep='')
                                
                        else:
                            print('\n'+str(acc),end='',sep='')
                        return_on_next=False
                    else:
                        if opr_type=='/\\':
                            print(str(acc),end='',sep='')
                        elif '¬' in opr_type:
                            
                            if operand!='':
                                print(str(chr(num % 256)),end='',sep='')
                            else:
                                
                                print(str(chr(acc % 256)),end='',sep='')
                                
                        else:
                            print(str(acc),end='',sep='')
                        
                case '<>': #return on next
                    if return_on_next==True:
                        print('')
                    return_on_next = True
                    
                case '<': #sta
                    if opr_type == "'":
                        memory[acc] = num
                    elif opr_type == "'//": #indirect technique
                        memory[acc] = memory[num]
                    else:
                        memory[num]=acc
                    
                                            
                case '>': #lda
                    if opr_type == "'":
                        acc = num
                    else:
                        if operand!='':
                            acc=memory[num]
                        
                        else:
                            acc=memory[acc]
                        
                case '->': #goto
                    if opr_type=='/\\':
                        l=num-1
                    elif opr_type=='>':
                        l=memory[num]-1
                    else:
                        l=num-1
                    
                case '>>': #in
                    value = input("")
                    if value.isnumeric():
                        acc=int(value)
                        
                    elif len(list(value)) > 1:
                        found = False
                        i = 0
                        while not found:
                            if memory.get(i) == None:
                                found = True
                            else:
                                i+=100
                        value=''.join([value[i] for i in range(len(value)-1,-1,-1)])
                        for char in range(len(value)):
                            memory[char+i] = ord(value[char])
                        acc=len(value)
                    
                case '<-/->': #clearscreen
                    os.system('cls')

                case '/->-/': #random
                    acc = random.randrange(num)
                    
                
                
                
        l+=1

        if debug:
            
            print(l, memory, acc, opcode, operand, condition_oper, cond, opr_type)
            print('')
            
except Exception as e:
    print(f'error raised in line {l}, {e}')