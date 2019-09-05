#For every variable in some LMAO code, it is read from or written to by some command. Many optimization techniques require knowledge of when a variable will be used to determine if some optimization is allowed. Write a function, called get_use_information that takes a multiline LMAOcode string and returns a dictionary where the keys are are variables (like "s3" or "a7") and the values are instances of the provided class VariableUses. This class has two attributes, a set of reads and and a set of writes. Reads and writes are tuples of the block number and the line number within the block.

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

def convert_to_basic_blocks(lmaocode):
    sanitized_lmaocode = sanitize(lmaocode)
    
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
    
def get_use_information(lmaocode):
    basic_blocks = convert_to_basic_blocks(lmaocode)
    
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
