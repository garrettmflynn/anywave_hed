def read(filepath):
    mrks = []
    try:
        fid = open(filepath, 'r')
        lines = fid.readlines()
        fid.close()

    except Exception as e:
        print(e)
        return


    # Check if marker file
    if (lines[0].strip() !=  '// AnyWave Marker File'):
        return
    
    # Grab marker info
    for line in lines[1:]: 
        [label, dummy, start, duration] = line.split()
        mrks.append([label, start, duration])

    return mrks