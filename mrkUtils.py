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
        mrk = line.split()
        del mrk[-3] # label, _, start, duration

        print(mrk[:-2])
        mrks.append([' '.join(mrk[:-2]), *mrk[-2:]])

    return mrks