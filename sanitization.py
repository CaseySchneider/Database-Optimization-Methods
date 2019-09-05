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
