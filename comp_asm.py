import sys, subprocess
import utils
from translations import between

f=None
try:
     f = sys.argv[1] #.ln file to open
except:
     f = input("e:")


if f != None and f != "":    
     with open(f,'r') as _:
          PROGRAM_BODY=_.readlines()
else: 
     raise RuntimeError("Please check validity of ln file")







'''
TODO: 
create jsonish of each line
using rules given in compile.py and struct.txt
'''



JSONISH = {'program':[]}



for i in range(len(PROGRAM_BODY)):
     line = PROGRAM_BODY[i]
     
     
     opcode = between(line,'_')
     operand = between(line,'=')
     condition = between(line,'|')
     typer= between(line,'+').replace("Â",'')
     if typer == "":
          typer=None
     

     JSONISH['program'].append(utils.generate_jsonish(opcode=opcode, operand=operand, condition=condition, dtype=typer))
     


print(JSONISH)

c_file_text = utils.json_to_c(JSONISH)

with open(f.replace(".ln",'.c'), 'w') as writable:
     writable.writelines(c_file_text)
     writable.close()

if sys.platform == "linux":
     subprocess.Popen(["gcc",f"{f.replace('.ln','.c')}","-o",f"{f.replace('.ln','')}"])
else:
     subprocess.Popen(["gcc",f"{f.replace('.ln','.c')}","-o",f"{f.replace('.ln','.exe')}"])