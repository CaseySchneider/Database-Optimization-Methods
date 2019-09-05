# DEAD CODE ELIMINATION
# You know the drill... write a function called "dead_code_elimination" that removes instructions with no effect on the execution.

#This includes NOPs and commands that write to a variable that can never be read from. This function should only make a single pass through the code (see the visible test cases).

# loop backwords through sanitized_lmaocode inptu and create a set of reads. eg a = b + c ... If the a is not in the set of reads, then you eliminate it and do not add b or c to the set of reads since you've eliminated that line
class VariableUses:
    def __init__(self, reads=None, writes=None):
        self.reads = reads if reads else set()
        self.writes = writes if writes else set()
    
    def __repr__(self):
        return f"VariableUses({self.reads}, {self.writes})"
    
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.reads != other.reads:
            return False
        return self.writes == other.writes



def sanitize(lmaocode_str):
    unsanitized_list = lmaocode_str.split('\n')
    sanitized_list = []
    for i in unsanitized_list:
        if i.strip() != '':
            incomplete_element = i.strip().split()
            almost_element = []
            
            space_added = False
            for i in incomplete_element:
                if i == "'":
                    if not(space_added):
                        almost_element.append("' '")
                        space_added = True
                else:
                    almost_element.append(i)
                

            complete_element = []
            for i in almost_element:
                if i == '#':
                    break
                else:
                    complete_element.append(i)
                    
            if len(complete_element) > 0:
                sanitized_list.append(complete_element)
                
            #sanitized_list.append(i.strip().split())
    #unsanitized_list = [i.strip().split() for i in unsanitized_list if i.strip() != '']
    
    return sanitized_list


def convert_to_basic_blocks(sanitized_lmaocode):
    # sanitized_lmaocode = sanitize(lmaocode)
    
    block_list = []
    
    block = []
    for i in sanitized_lmaocode:
        if i[0] == "JUMP" or i[0] == "JUMP_IF_N0" or i[0] == "JUMP_IF_0":
            block.append(i)
            block_list.append(block)
            block = []
        elif i[0][-1] == ":":
            if len(block) > 0:
                block_list.append(block)
            block = []
            block.append(i)
        else:
            block.append(i)
            
    if len(block) > 0:
        block_list.append(block)
        
    return block_list
    




def get_use_information(lmaocode): # lmaocode is sanitized
    basic_blocks = convert_to_basic_blocks(lmaocode) # lmaocode is sanitized
    
    #print("im the blocks: ", basic_blocks)
    
    # keys: variables (like "s7" or "a3")
    # values: VariableUses instances (Set(reads), Set(writes))
    # reads/writes == Tuple(block#, line#)
    variable_usage = dict()
    
    # i = block
    for i in range(len(basic_blocks)):
        # j = line 
        for j in range(len(basic_blocks[i])):
            # if its a label
            if len(basic_blocks[i][j]) == 1:
                continue
            # k = param
            for k in range(len(basic_blocks[i][j]) - 1):
                
                
                if basic_blocks[i][j][0] == "AR_SET_SIZE":
                    if basic_blocks[i][j][1] in variable_usage:
                        if variable_usage[basic_blocks[i][j][1]].writes != None:
                            variable_usage[basic_blocks[i][j][1]].writes.add((i, j))
                        else:
                            variable_usage[basic_blocks[i][j][1]] = VariableUses(writes={(i, j)})
                    else:
                        variable_usage[basic_blocks[i][j][1]] = VariableUses(writes={(i, j)})
                    
                    if basic_blocks[i][j][2][0] == 's':
                        if basic_blocks[i][j][2] in variable_usage:
                            if variable_usage[basic_blocks[i][j][2]].reads != None:
                                variable_usage[basic_blocks[i][j][2]].reads.add((i, j))
                            else:
                                variable_usage[basic_blocks[i][j][2]] = VariableUses(reads={(i, j)})
                        else:
                            variable_usage[basic_blocks[i][j][2]] = VariableUses(reads={(i, j)})
                    

                
                elif basic_blocks[i][j][0] == "AR_SET_IDX":
                    if basic_blocks[i][j][1] in variable_usage:
                        if variable_usage[basic_blocks[i][j][1]].writes != None:
                            variable_usage[basic_blocks[i][j][1]].writes.add((i, j))
                        else:
                            variable_usage[basic_blocks[i][j][1]] = VariableUses(writes={(i, j)})
                    else:
                        variable_usage[basic_blocks[i][j][1]] = VariableUses(writes={(i, j)})
                        
                    if basic_blocks[i][j][2][0] == 's':
                        if basic_blocks[i][j][2] in variable_usage:
                            if variable_usage[basic_blocks[i][j][2]].reads != None:
                                variable_usage[basic_blocks[i][j][2]].reads.add((i, j))
                            else:
                                variable_usage[basic_blocks[i][j][2]] = VariableUses(reads={(i, j)})
                        else:
                            variable_usage[basic_blocks[i][j][2]] = VariableUses(reads={(i, j)})




                else:
                    if basic_blocks[i][j][k][0] == 'a' or basic_blocks[i][j][k][0] == 's':
                        if basic_blocks[i][j][k] in variable_usage:
                            if variable_usage[basic_blocks[i][j][k]].reads != None:
                                variable_usage[basic_blocks[i][j][k]].reads.add((i, j))
                            else:
                                variable_usage[basic_blocks[i][j][k]] = VariableUses(reads={(i, j)})
                        else:
                            variable_usage[basic_blocks[i][j][k]] = VariableUses(reads={(i, j)})
                        


            # must guard against labels
            if basic_blocks[i][j][-1][0] == 'a' or basic_blocks[i][j][-1][0] == 's':
                
                if basic_blocks[i][j][0] == "OUT_CHAR" or basic_blocks[i][j][0] == "OUT_NUM":
                        if basic_blocks[i][j][-1] in variable_usage:
                            if variable_usage[basic_blocks[i][j][-1]].reads != None:
                                variable_usage[basic_blocks[i][j][-1]].reads.add((i, j))
                            else:
                                variable_usage[basic_blocks[i][j][-1]] = VariableUses(reads={(i, j)})
                        else:
                            variable_usage[basic_blocks[i][j][-1]] = VariableUses(reads={(i, j)})

                elif basic_blocks[i][j][0] == "AR_SET_SIZE":
                        if basic_blocks[i][j][-1] in variable_usage:
                            if variable_usage[basic_blocks[i][j][-1]].reads != None:
                                variable_usage[basic_blocks[i][j][-1]].reads.add((i, j))
                            else:
                                variable_usage[basic_blocks[i][j][-1]] = VariableUses(reads={(i, j)})
                        else:
                            variable_usage[basic_blocks[i][j][-1]] = VariableUses(reads={(i, j)})

                elif basic_blocks[i][j][0] == "AR_SET_IDX":
                        if basic_blocks[i][j][-1] in variable_usage:
                            if variable_usage[basic_blocks[i][j][-1]].reads != None:
                                variable_usage[basic_blocks[i][j][-1]].reads.add((i, j))
                            else:
                                variable_usage[basic_blocks[i][j][-1]] = VariableUses(reads={(i, j)})
                        else:
                            variable_usage[basic_blocks[i][j][-1]] = VariableUses(reads={(i, j)})



                elif basic_blocks[i][j][0] == "JUMP":
                        continue

                elif basic_blocks[i][j][0] == "JUMP_IF_N0":
                        if basic_blocks[i][j][1] in variable_usage:
                            if variable_usage[basic_blocks[i][j][1]].reads != None:
                                variable_usage[basic_blocks[i][j][1]].reads.add((i, j))
                            else:
                                variable_usage[basic_blocks[i][j][1]] = VariableUses(reads={(i, j)})
                        else:
                            variable_usage[basic_blocks[i][j][1]] = VariableUses(reads={(i, j)})

                elif basic_blocks[i][j][0] == "JUMP_IF_0":
                        if basic_blocks[i][j][1] in variable_usage:
                            if variable_usage[basic_blocks[i][j][1]].reads != None:
                                variable_usage[basic_blocks[i][j][1]].reads.add((i, j))
                            else:
                                variable_usage[basic_blocks[i][j][1]] = VariableUses(reads={(i, j)})
                        else:
                            variable_usage[basic_blocks[i][j][1]] = VariableUses(reads={(i, j)})

                else:
                    if basic_blocks[i][j][-1] in variable_usage:
                        if variable_usage[basic_blocks[i][j][-1]].writes != None:
                            variable_usage[basic_blocks[i][j][-1]].writes.add((i, j))
                        else:
                            variable_usage[basic_blocks[i][j][-1]] = VariableUses(writes={(i, j)})
                    else:
                        variable_usage[basic_blocks[i][j][-1]] = VariableUses(writes={(i, j)})
                        
                    







    return variable_usage

'''
# VARIABLES READ IN ANOTHER BLOCK ARE ALIVE

print()
print()
print()
print("# VARIABLES READ IN ANOTHER BLOCK ARE ALIVE")
lmaocode = r"""
VAL_COPY s7 s9
OUT_NUM s9
label:
VAL_COPY 5 s7
ADD 3 4 s10
ADD s10 s14 s19
"""
sanitized_lmaocode = deadcode.sanitize(lmaocode)
result = deadcode.dead_code_elimination(sanitized_lmaocode)
pprint(result)
expected = [['VAL_COPY', 's7', 's9'],
 ['OUT_NUM', 's9'],
 ['label:'],
 ['VAL_COPY', '5', 's7'],
 ['ADD', '3', '4', 's10']]
#self.assertEqual(expected, result)
'''



def dead_code_elimination(sanitized):
    alive_vars = set()
    clean_code = []
    use_info = get_use_information(sanitized)
    basic_blocks = convert_to_basic_blocks(sanitized)





    for j in range(len(basic_blocks)-1, -1, -1):
        for i in reversed(basic_blocks[j]):
        
            # if a stateful effect, then do not remove
            if i[0] == "OUT_NUM" or i[0] == "OUT_CHAR" or i[0] == "JUMP" or i[0] == "JUMP_IF_N0" or i[0] == "JUMP_IF_0":
                clean_code.append(i)
                # add its constituents to alive vars
                alive_vars.add(i[1])


            elif i[0] == "NOP":
                pass

            elif len(i) == 1:
                clean_code.append(i)


            elif not(i[0] == "RANDOM" or i[0] == "POP" or i[0] == "IN_CHAR" or i[0] == "PUSH"):

                # if the result is live
                if i[-1] in alive_vars:
                    # then add its contituents to alive vars
                    if len(i) == 4:
                        alive_vars.add(i[1])
                        alive_vars.add(i[2])
                    elif len(i) == 3:
                        alive_vars.add(i[1])

                    # and add the line
                    clean_code.append(i)

                else:
                    # add the line's consituents to alive vars
                    if len(i) == 4:
                        alive_vars.add(i[1])
                        alive_vars.add(i[2])
                    elif len(i) == 3:
                        alive_vars.add(i[1])






                    read_in_another_block = False


                    for k in use_info[i[-1]].reads:
                        # if the var is read in another block
                        if k[0] != j:
                            print("AHHHHHHHHHHHHHH")
                            # add the line
                            clean_code.append(i)
                            break
                        
                        # eliminate the line
                        # NOT appending to clean_code

            else:
                clean_code.append(i)
    


    reverse_clean_code = []
    for i in reversed(clean_code):
        reverse_clean_code.append(i)

    return reverse_clean_code




    
