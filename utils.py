from translations import *



def generate_jsonish(*, opcode:str, operand:str, condition:str="", dtype:str|None=None) -> dict:
    
     p_opcode = OPCODES.get(opcode)
     p_operand = conv_denary(operand)
     if isinstance(p_operand, int) and p_operand < 0:
          p_operand = 16384 + p_operand


     conjson = None
     if condition != "":
          _neg = False
          if "¬" in condition:
               _neg = True
               condition=condition.replace("¬",'').replace("Â",'')
          print(condition)
          
          _temp_p_cond_opcode = between(condition, "'")
          _temp_p_cond_operand = between(condition, '"')
          print(_temp_p_cond_opcode,_temp_p_cond_operand)
          p_cond_opcode = CONDITION_OPCODES.get(_temp_p_cond_opcode)
          p_cond_operand = conv_denary(_temp_p_cond_operand)
          

          if p_cond_opcode == None or (p_cond_operand == '' and p_cond_opcode in ['GREATER_THAN_EQ', 'LESS_THAN_EQ', 'EQ']):
               raise SyntaxError(f"Insufficient condition formation, {p_cond_opcode, p_cond_operand}")
          
          
          


          conjson = {
               "logic":"NOT" if _neg else None,
               "comparison":p_cond_opcode,
               "value":p_cond_operand,
          }






     return {"opcode":p_opcode, "operand":p_operand, "condition": conjson, "declared_type":ADDRESSING_MODES[dtype] if dtype else dtype}
    
def generate_typed_jsonish(*, dtype:ADDRESSING_MODE) -> dict: #throws TypeError if incorrect type given
     return {"declared_type":dtype}






def json_to_c(json_program, ram_size:int = 16384):
     c_lines = [
          "#include <stdio.h>\n",

          "int main() {\n",
          f"int ram[{ram_size}];\n",
          "int accumulator = 0;\n"
     ]
     
     
     

     dtype = "INT"
     code = ""
     
     for i, instr in enumerate(json_program["program"]):
          instr:dict
          code = ""
          conditioncode = ""

          


          label = f"line{i}:\n"
          next_label = f"goto line{i+1};" if len(json_program['program'])-1 != i else "return 0; }"
          condition = instr["condition"]
          if condition != None:
               
               cond_opcode = condition.get("comparison")
               cond_opcode = CONDITION_OPERATORS.get(cond_opcode)

               cond_value = condition.get("value")
               
               cond_logic = condition.get("logic")

               cnum = f"ram[{cond_value}]" if dtype == "RAM" else cond_value
               conditioncode = f"if ({'!' if cond_logic == 'NOT' else ''}(accumulator {cond_opcode} {cnum})) " + " {"
          
          
          type_change = instr.get("declared_type")
          if type_change != None and type_change != "":
               dtype = type_change
               


          
          match instr["opcode"]:
               case "IN":
                    code = 'scanf("%d", &accumulator);'

               case "OUT":
                    print(instr['operand'], dtype)
                    if dtype == "INT":
                         code = f'printf("%d", accumulator);'
                    elif dtype == "CHAR":
                         code = f'printf("%c", {instr["operand"] if (dtype == "CHAR" and instr["operand"] != "") else "accumulator"});'

               case "STA":
                    if dtype == "DIRECT":
                         code = f"ram[accumulator] = {instr['operand']};"
                    elif dtype == "INDIRECT":
                         code = f"ram[accumulator] = ram[{instr['operand']}];"
                    else:
                         code = f"ram[{instr['operand']}] = accumulator;"

               case "LDA":
                    if dtype == "DIRECT":
                         code = f"accumulator = {instr['operand']};"
                    else:
                         if instr['operand'] != '':
                              code = f"accumulator = ram[{instr['operand']}];"
                         else:
                              code = "accumulator = ram[accumulator];"
               
               case "ADD":
                    if dtype == "INT":
                         code = f"accumulator += {instr['operand']};"
                    else:
                         code = f"accumulator += ram[{instr['operand']}];"
               
               case "SUB":
                    if dtype == "INT":
                         code = f"accumulator -= {instr['operand']};"
                    else:
                         code = f"accumulator -= ram[{instr['operand']}];"
               
               case "RETURN":
                    code = r'printf("\n");'

               case "GOTO":
                    code = f"goto line{instr['operand']-1};"
                    
               
          
               
          if conditioncode != "":
               c_lines.append(f"{label}  {conditioncode}{code + '}'}\n    {next_label}\n")
          else:
               c_lines.append(f"{label}    {code}\n    {next_label}\n")
     return c_lines
