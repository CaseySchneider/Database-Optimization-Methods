# make multiple optimization passes using the previously described functions in order:
#   [algebraic_simplification, 
#    constant_folding, 
#    copy_propagation, 
#    dead_code_elimination] 
# until no further improvement is possible.

# Write a function called "optimize" that takes a multiline LMAOcode string and returns a multiline LMAOcode string that is optimized using all the functions described above. The optimize function should make multiple optimization passes using the previously described functions in order [algebraic_simplification, constant_folding, copy_propagation, dead_code_elimination] until no further improvement is possible.



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
    #sanitized_lmaocode = sanitize(lmaocode)
    
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



def algebraic_simplification(sanitized):

    # not handling multiplication by 1

    simplified = []

    for i in sanitized:
        if i[0] == "ADD":
            if i[2] == "0":
                if i[1] == i[3]:
                    simplified.append(["NOP"])
                else:
                    simplified.append(["VAL_COPY", i[1], i[3]])
            elif i[1] == "0":
                if i[2] == i[3]:
                    simplified.append(["NOP"])
                else:
                    simplified.append(["VAL_COPY", i[2], i[3]])
            else:
                simplified.append(i)

            
        elif i[0] == "SUB":
            if i[2] == "0":
                if i[1] == i[3]:
                    simplified.append(["NOP"])
                else:
                    simplified.append(["VAL_COPY", i[1], i[3]])
            elif i[1] == "0":
                if i[2] == i[3]:
                    simplified.append(["NOP"])
                else:
                    simplified.append(["VAL_COPY", i[2], i[3]])
            else:
                simplified.append(i)


                    
        elif i[0] == "DIV":
            if i[1] == "0":
                simplified.append(["VAL_COPY", "0", i[3]])
            elif i[2] == "1":
                simplified.append(["VAL_COPY", i[1], i[3]])
            else:
                simplified.append(i)


        elif i[0] == "MULT":
            if i[1] == "0" or i[2] == "0":
                simplified.append(["VAL_COPY", "0", i[3]])
            else:
                simplified.append(i)

        

        elif i[0] == "VAL_COPY":
            if i[1] == i[2]:
                simplified.append(["NOP"])
            else:
                simplified.append(i)

        else:
            simplified.append(i)



    return simplified

def constant_folding(sanitized):
    folded = []

    for i in sanitized:
        if i[0] == "ADD":
            if i[1][0] != "s" and i[2][0] != "s":
                if "." in i[1] or "." in i[2]:
                    result = float(i[1]) + float(i[2])
                else:
                    result = int(i[1]) + int(i[2])
                folded.append(["VAL_COPY", str(result), i[3]])
            else:
                folded.append(i)

            
        elif i[0] == "SUB":
            if i[1][0] != "s" and i[2][0] != "s":
                if "." in i[1] or "." in i[2]:
                    result = float(i[1]) - float(i[2])
                else:
                    result = int(i[1]) - int(i[2])
                folded.append(["VAL_COPY", str(result), i[3]])
            else:
                folded.append(i)


                    
        elif i[0] == "DIV":
            if i[1][0] != "s" and i[2][0] != "s":
                if "." in i[1] or "." in i[2]:
                    result = float(i[1]) / float(i[2])
                else:
                    result = int(i[1]) // int(i[2])
                folded.append(["VAL_COPY", str(result), i[3]])
            else:
                folded.append(i)


        elif i[0] == "MULT":
            if i[1][0] != "s" and i[2][0] != "s":
                if "." in i[1] or "." in i[2]:
                    result = float(i[1]) * float(i[2])
                else:
                    result = int(i[1]) * int(i[2])
                folded.append(["VAL_COPY", str(result), i[3]])
            else:
                folded.append(i)



        elif i[0] == "JUMP_IF_0":

            if i[1][0] == "'":
                folded.append(["NOP"])

            elif i[1][0] != "s":
                if int(i[1]) == 0:
                    folded.append(["JUMP", i[2]])
                else:
                    folded.append(["NOP"])
            else:
                folded.append(i)



        elif i[0] == "JUMP_IF_N0":

            if i[1][0] == "'":
                folded.append(["JUMP", i[2]])

            elif i[1][0] != "s":
                if int(i[1]) != 0:
                    folded.append(["JUMP", i[2]])
                else:
                    folded.append(["NOP"])
            else:
                folded.append(i)



        # TEST_EQU '4' 4 s89


        elif i[0] == "TEST_EQU":

            if (i[1][0] == "'" and i[2][0] != "'") or (i[1][0] != "'" and i[2][0] == "'"):
                folded.append(["VAL_COPY", "0", i[3]])

            elif i[1][0] == "'" and i[2][0] == "'":
                if i[1] == i[2]:
                    folded.append(["VAL_COPY", "1", i[3]])
                else:
                    folded.append(["VAL_COPY", "0", i[3]])
                
            elif i[1][0] != "s" and i[2][0] != "s":
                if float(i[1]) == float(i[2]):
                    folded.append(["VAL_COPY", "1", i[3]])
                else:
                    folded.append(["VAL_COPY", "0", i[3]])
            else:
                folded.append(i)


        elif i[0] == "TEST_NEQU":

            if (i[1][0] == "'" and i[2][0] != "'") or (i[1][0] != "'" and i[2][0] == "'"):
                folded.append(["VAL_COPY", "1", i[3]])

            elif i[1][0] == "'" and i[2][0] == "'":
                if i[1] == i[2]:
                    folded.append(["VAL_COPY", "0", i[3]])
                else:
                    folded.append(["VAL_COPY", "1", i[3]])

            elif i[1][0] != "s" and i[2][0] != "s":
                if float(i[1]) != float(i[2]):
                    folded.append(["VAL_COPY", "1", i[3]])
                else:
                    folded.append(["VAL_COPY", "0", i[3]])
            else:
                folded.append(i)




        elif i[0] == "TEST_LTE":
            if i[1][0] != "s" and i[2][0] != "s":
                if float(i[1]) <= float(i[2]):
                    folded.append(["VAL_COPY", "1", i[3]])
                else:
                    folded.append(["VAL_COPY", "0", i[3]])
            else:
                folded.append(i)


        elif i[0] == "TEST_GTE":
            if i[1][0] != "s" and i[2][0] != "s":
                if float(i[1]) >= float(i[2]):
                    folded.append(["VAL_COPY", "1", i[3]])
                else:
                    folded.append(["VAL_COPY", "0", i[3]])
            else:
                folded.append(i)
















        else:
            folded.append(i)





    return folded
    folded = []

    for i in sanitized:
        if i[0] == "ADD":
            if i[1][0] != "s" and i[2][0] != "s":
                result = float(i[1]) + float(i[2])
                folded.append(["VAL_COPY", str(result), i[3]])
            else:
                folded.append(i)

            
        elif i[0] == "SUB":
            if i[1][0] != "s" and i[2][0] != "s":
                result = float(i[1]) - float(i[2])
                folded.append(["VAL_COPY", str(result), i[3]])
            else:
                folded.append(i)


                    
        elif i[0] == "DIV":
            if i[1][0] != "s" and i[2][0] != "s":
                result = float(i[1]) / float(i[2])
                folded.append(["VAL_COPY", str(result), i[3]])
            else:
                folded.append(i)


        elif i[0] == "MULT":
            if i[1][0] != "s" and i[2][0] != "s":
                result = float(i[1]) * float(i[2])
                folded.append(["VAL_COPY", str(result), i[3]])
            else:
                folded.append(i)



        elif i[0] == "JUMP_IF_0":

            if i[1][0] == "'":
                folded.append(["NOP"])

            elif i[1][0] != "s":
                if int(i[1]) == 0:
                    folded.append(["JUMP", i[2]])
                else:
                    folded.append(["NOP"])
            else:
                folded.append(i)



        elif i[0] == "JUMP_IF_N0":

            if i[1][0] == "'":
                folded.append(["JUMP", i[2]])

            elif i[1][0] != "s":
                if int(i[1]) != 0:
                    folded.append(["JUMP", i[2]])
                else:
                    folded.append(["NOP"])
            else:
                folded.append(i)



        # TEST_EQU '4' 4 s89


        elif i[0] == "TEST_EQU":

            if (i[1][0] == "'" and i[2][0] != "'") or (i[1][0] != "'" and i[2][0] == "'"):
                folded.append(["VAL_COPY", "0", i[3]])

            elif i[1][0] == "'" and i[2][0] == "'":
                if i[1] == i[2]:
                    folded.append(["VAL_COPY", "1", i[3]])
                else:
                    folded.append(["VAL_COPY", "0", i[3]])
                
            elif i[1][0] != "s" and i[2][0] != "s":
                if float(i[1]) == float(i[2]):
                    folded.append(["VAL_COPY", "1", i[3]])
                else:
                    folded.append(["VAL_COPY", "0", i[3]])
            else:
                folded.append(i)


        elif i[0] == "TEST_NEQU":

            if (i[1][0] == "'" and i[2][0] != "'") or (i[1][0] != "'" and i[2][0] == "'"):
                folded.append(["VAL_COPY", "1", i[3]])

            elif i[1][0] == "'" and i[2][0] == "'":
                if i[1] == i[2]:
                    folded.append(["VAL_COPY", "0", i[3]])
                else:
                    folded.append(["VAL_COPY", "1", i[3]])

            elif i[1][0] != "s" and i[2][0] != "s":
                if float(i[1]) != float(i[2]):
                    folded.append(["VAL_COPY", "1", i[3]])
                else:
                    folded.append(["VAL_COPY", "0", i[3]])
            else:
                folded.append(i)




        elif i[0] == "TEST_LTE":
            if i[1][0] != "s" and i[2][0] != "s":
                if float(i[1]) <= float(i[2]):
                    folded.append(["VAL_COPY", "1", i[3]])
                else:
                    folded.append(["VAL_COPY", "0", i[3]])
            else:
                folded.append(i)


        elif i[0] == "TEST_GTE":
            if i[1][0] != "s" and i[2][0] != "s":
                if float(i[1]) >= float(i[2]):
                    folded.append(["VAL_COPY", "1", i[3]])
                else:
                    folded.append(["VAL_COPY", "0", i[3]])
            else:
                folded.append(i)


        else:
            folded.append(i)


    return folded

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

def dead_code_elimination(sanitized):
    alive_vars = set()
    clean_code = []
    use_info = get_use_information(sanitized)
    basic_blocks = convert_to_basic_blocks(sanitized)





    for j in range(len(basic_blocks)-1, -1, -1):
        for i in reversed(basic_blocks[j]):
        

            if i[0] == "PUSH" or i[0] == "POP":
                clean_code.append(i)
                alive_vars.add(i[1])
            # if a stateful effect, then do not remove
            elif i[0] == "OUT_NUM" or i[0] == "OUT_CHAR" or i[0] == "JUMP" or i[0] == "JUMP_IF_N0" or i[0] == "JUMP_IF_0":
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

                        

                    for k in use_info[i[-1]].reads:
                        # if the var is read in another block
                        if k[0] != j:
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

                        

                    for k in use_info[i[-1]].reads:
                        # if the var is read in another block
                        if k[0] != j:
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



def optimize(lmaocode):
    optimized = sanitize(lmaocode)
    basic_blocks = convert_to_basic_blocks(optimized)
    
    for i in range(2):
        optimized = algebraic_simplification(optimized)
        print()
        print()
        print()
        print()
        print("After algebraic simplification: \n")
        for i in optimized:
            print(i)
        print()
        optimized = constant_folding(optimized)
        print("After constant_folding: \n")
        for i in optimized:
            print(i)
        print()
        optimized = copy_propagation(optimized)
        print()
        print("After copy_propagation: \n")
        for i in optimized:
            print(i)
        print()
        optimized = dead_code_elimination(optimized)
        print("After dead_code_elimination: \n")
        for i in optimized:
            print(i)
        print()
        print()
        print()
        print()

    lmaocode_return = ""

    # through lines
    for i in optimized:
        # through params
        lmaocode_return += " ".join(i)
        lmaocode_return += "\n"
    
    #print(lmaocode_return)

    return lmaocode_return
