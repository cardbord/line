from typing import Literal

def between(line:str,char:str) -> str:
    char1 = line.find(char)
    if char1==-1:
        return ''

    return line[char1+1:line.find(char,char1+1)]

def conv_ln(num:int):
    _temp = str(bin(num))
    b = '0'+_temp.replace('0b','')
    b=b.replace('0','/')
    b=b.replace('1','\\')
    
    return b

def conv_denary(ln:str) -> int|Literal[""]:
    if ln == "":
        return ""

    b = ln.replace('/','0')
    b = b.replace('\\','1')
    
    b = bin_to_int(b)

    return b

def bin_to_int(binary:str) -> int:
    temp=0
    for c in range(len(binary)-1,-1, -1):
        if binary[c] == '1':
            temp+= 2**(len(binary)-1-c) if c != 0 else -(2**(len(binary)-1-c))
    return temp


REV_OPCODES = {
     "ADD":"--",
     "SUB":"-",
     "STA":"<",
     "LDA":">",
     "OUT":"<<",
     "IN":">>",
     "GOTO":"->",
     "RETURN":"<>",
     "RAND":"/->-/",
     "CLEAR":"<-/->"
}
OPCODES = {v:k for k,v in REV_OPCODES.items()}
ADDRESSING_MODE = Literal["/\\",">","¬","'//","'"]
ADDRESSING_MODES = {
     "/\\":"INT",
     ">":"RAM",
     "¬":"CHAR",
     "'//":"INDIRECT",
     "'":"DIRECT"
}
CONDITION_OPCODES = {
     "/":"BRZ",
     "\\":"BRP",
     ">/":"GREATER_THAN_EQ",
     "\\<":"LESS_THAN_EQ",
     "---":"EQ"
}

CONDITION_OPERATORS = {
    "BRZ":"==0",
    "BRP":">0",
    "GREATER_THAN_EQ":">=",
    "LESS_THAN_EQ":"<=",
    "EQ":"=="
}

