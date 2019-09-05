#Write a function, called convert_to_basic_blocks, that takes a LMAOcode string and returns a list of basic blocks. Each basic block is a list of sanitized lines of LMAOcode belonging to the block.

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
    
