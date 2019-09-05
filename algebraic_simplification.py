
# apply the algebraic identities for the 4 math operations (ADD, SUB, MULT, DIV), and then simplify to VAL_COPY's or NOP's
# VAL_COPY's that merely copy the same value onto itself must also be replaced with a NOP.

# Write a function called "algebraic_simplification" that takes a sanitized LMAOcode list (the output from the first function in this project), and returns a sanitized list as well. But the returned list should apply the algebraic identities for the 4 math operations (ADD, SUB, MULT, DIV), and then simplify to VAL_COPY's or NOP's. Also, VAL_COPY's that merely copy the same value onto itself must also be replaced with a NOP.

 

# Example:

# ADD s1 0 s3 -> VAL_COPY s1 s3

# SUB s1 0 s1 -> NOP

# VAL_COPY s78 s78 -> NOP


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
