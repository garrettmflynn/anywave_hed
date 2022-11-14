def read(fname):
    mrks = []
    try:
        fid = open(fname, 'r')
        lines = fid.readlines()
        fid.close()

    except Exception as e:
        return


    if (lines[0].trim() !=  '// AnyWave Marker File'):
        print('Not an AnyWave marker file...')
        return

    # [label, dummy, start, duration] = textread(fname, '%s %d %f %f', 'delimiter', char(9), 'headerlines', 1);

    # mrks = horzcat(label, cellfun(@num2str, num2cell(start),'UniformOutput',false), cellfun(@num2str, num2cell(duration),'UniformOutput',false));