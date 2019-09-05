# return the LMAOcode instructions after performing constant folding on each line. 
# Be sure you are careful with float and character literals. 

#Write a function called "constant_folding" that takes a returns a sanitized list of LMAOcode instructions (similar to "algebraic_simplification"). It should return the LMAOcode instructions after performing constant folding on each line. Be sure you are careful with float and character literals. 

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



# if its an int do int arithmetic
# if its a float do float arithmetic


def constant_folding(sanitized):
    folded = []

    for i in sanitized:
        if i[0] == "ADD":
            if i[1][0] != "s" and i[2][0] != "s":
                if "." in i[1]:
                    result = float(i[1]) + float(i[2])
                else:
                    result = int(i[1]) + int(i[2])
                    
                folded.append(["VAL_COPY", str(result), i[3]])
            else:
                folded.append(i)

            
        elif i[0] == "SUB":
            if i[1][0] != "s" and i[2][0] != "s":
                if "." in i[1]:
                    result = float(i[1]) - float(i[2])
                else:
                    result = int(i[1]) - int(i[2])
                folded.append(["VAL_COPY", str(result), i[3]])
            else:
                folded.append(i)


                    
        elif i[0] == "DIV":
            if i[1][0] != "s" and i[2][0] != "s":
                if "." in i[1]:
                    result = float(i[1]) / float(i[2])
                else:
                    result = int(i[1]) / int(i[2])
                folded.append(["VAL_COPY", str(result), i[3]])
            else:
                folded.append(i)


        elif i[0] == "MULT":
            if i[1][0] != "s" and i[2][0] != "s":
                if "." in i[1]:
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


