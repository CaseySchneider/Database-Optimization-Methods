# Write a function called "copy_propagation" that takes and returns sanitized LMAO code instructions (like all the other optimization algorithms).  The returned list of instructions should have copy propagation performed.



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
                else:
                    if basic_blocks[i][j][k][0] == 'a' or basic_blocks[i][j][k][0] == 's':
                        if basic_blocks[i][j][k] in variable_usage:
                            if variable_usage[basic_blocks[i][j][k]].reads != None:
                                variable_usage[basic_blocks[i][j][k]].reads.add((i, j))
                            else:
                                variable_usage[basic_blocks[i][j][k]] = VariableUses(reads={(i, j)})
                        else:
                            variable_usage[basic_blocks[i][j][k]] = VariableUses(reads={(i, j)})
                        
            if basic_blocks[i][j][-1][0] == 'a' or basic_blocks[i][j][-1][0] == 's':
                
                if basic_blocks[i][j][0] == "OUT_CHAR" or basic_blocks[i][j][0] == "OUT_NUM":
                        if basic_blocks[i][j][-1] in variable_usage:
                            if variable_usage[basic_blocks[i][j][-1]].reads != None:
                                variable_usage[basic_blocks[i][j][-1]].reads.add((i, j))
                            else:
                                variable_usage[basic_blocks[i][j][-1]] = VariableUses(reads={(i, j)})
                        else:
                            variable_usage[basic_blocks[i][j][-1]] = VariableUses(reads={(i, j)})
                    
                else:
                    if basic_blocks[i][j][-1] in variable_usage:
                        if variable_usage[basic_blocks[i][j][-1]].writes != None:
                            variable_usage[basic_blocks[i][j][-1]].writes.add((i, j))
                        else:
                            variable_usage[basic_blocks[i][j][-1]] = VariableUses(writes={(i, j)})
                    else:
                        variable_usage[basic_blocks[i][j][-1]] = VariableUses(writes={(i, j)})
                        
    return variable_usage


# only allowed within (not between) blocks
def copy_propagation(sanitized):
    copied = []
    # variable_usage = get_use_information(sanitized)
    basic_blocks = convert_to_basic_blocks(sanitized)


    # # go through the variables
    # for i in variable_usage:
        # # if a variable is read that has had a VAL_COPY copy to that variable, use the VAL_COPY A B ( A argument ) instead of the variable that was trying to be read
        # for j in i.reads





    # i = block
    for i in range(len(basic_blocks)):
        # key : result
        # value : copied from
        copy_dict = dict()
        # j = line 
        for j in range(len(basic_blocks[i])):
            # k = param
            if basic_blocks[i][j][0] == "VAL_COPY":
                if basic_blocks[i][j][1] in copy_dict:
                    copied.append(["VAL_COPY", copy_dict[basic_blocks[i][j][1]], basic_blocks[i][j][2]])
                    if basic_blocks[i][j][2] in copy_dict:
                        del copy_dict[basic_blocks[i][j][2]]
                else:
                    print("OOLALALA")
                    copied.append(basic_blocks[i][j])
                    copy_dict[basic_blocks[i][j][2]] = basic_blocks[i][j][1]
                    #if basic_blocks[i][j][2] in copy_dict:
                    #    del copy_dict[basic_blocks[i][j][2]]

            elif len(basic_blocks[i][j]) == 4:
                # if left in dict
                if basic_blocks[i][j][1] in copy_dict:
                    # if both in dict
                    if basic_blocks[i][j][2] in copy_dict:
                        copied.append([basic_blocks[i][j][0], copy_dict[basic_blocks[i][j][1]], copy_dict[basic_blocks[i][j][2]], basic_blocks[i][j][3]])
                        if basic_blocks[i][j][3] in copy_dict:
                            del copy_dict[basic_blocks[i][j][3]]
                    else:
                        copied.append([basic_blocks[i][j][0], copy_dict[basic_blocks[i][j][1]], basic_blocks[i][j][2], basic_blocks[i][j][3]])
                        if basic_blocks[i][j][3] in copy_dict:
                            del copy_dict[basic_blocks[i][j][3]]
                # right one is in dict
                elif basic_blocks[i][j][2] in copy_dict:
                    copied.append([basic_blocks[i][j][0], basic_blocks[i][j][1], copy_dict[basic_blocks[i][j][2]], basic_blocks[i][j][3]])
                    if basic_blocks[i][j][3] in copy_dict:
                        del copy_dict[basic_blocks[i][j][3]]
                else:
                    copied.append(basic_blocks[i][j])
                    if basic_blocks[i][j][3] in copy_dict:
                        del copy_dict[basic_blocks[i][j][3]]

            elif len(basic_blocks[i][j]) == 3:
                if basic_blocks[i][j][1] in copy_dict:
                    copied.append([basic_blocks[i][j][0], copy_dict[basic_blocks[i][j][1]], basic_blocks[i][j][2]])
                    if basic_blocks[i][j][2] in copy_dict:
                        del copy_dict[basic_blocks[i][j][2]]
                else:
                    copied.append(basic_blocks[i][j])
                    if basic_blocks[i][j][2] in copy_dict:
                        del copy_dict[basic_blocks[i][j][2]]


            elif basic_blocks[i][j][0] == "OUT_NUM" or basic_blocks[i][j][0] == "OUT_CHAR" or basic_blocks[i][j][0] == "PUSH":
                print("AHHHHHH: ", copy_dict)
                if basic_blocks[i][j][1] in copy_dict:
                    copied.append([basic_blocks[i][j][0], copy_dict[basic_blocks[i][j][1]]])
                else:
                    copied.append(basic_blocks[i][j])


            else:
                copied.append(basic_blocks[i][j])
                if basic_blocks[i][j][-1] in copy_dict:
                        del copy_dict[basic_blocks[i][j][-1]]

                    
                



        # if either of the read arguments in the command have been the result of a VAL_COPY, use the read arguments of the VAL_COPY instead



    return copied
