def read(filepath):
    mrks = []
    try:
        with open(filepath, 'r') as fid:    
            lines = [ line.strip() for line in fid ]
            fid.close()

    except Exception as e:
        print(e)
        return


    # Check if marker file
    if (len(lines) == 0 or lines[0].strip() !=  '// AnyWave Marker File'):
        print('Not a valid marker file', filepath)
        return
    
    # Grab marker info
    for line in lines[1:]: 
        mrk = line.split()
        del mrk[-3] # label, _, start, duration
        mrks.append([' '.join(mrk[:-2]), *mrk[-2:]])

    return mrks


def convertToString(cell):
    return str(cell)
    
def convertToLine(mrk):
    return ' '.join(map(convertToString, mrk))

def unique(list1):
 
    # initialize a null list
    unique_list = []
 
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)

    return unique_list

def write(filepath, mrks):
    with open(filepath, 'r') as fid:    
        lines = [ line.strip() for line in fid ]
        fid.close()

        if (len(lines) == 0 or lines[0].strip() !=  '// AnyWave Marker File'):
            lines = ['// AnyWave Marker File', *lines]
        
        lines = [*lines, *map(convertToLine, mrks)]

        with open(filepath, 'w') as fid:    

            unique_list = unique(lines)

            fid.writelines(line + '\n' for line in unique_list)

