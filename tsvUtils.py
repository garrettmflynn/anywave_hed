
from pathlib import Path;
import pandas as pd;
import jsonUtils

def createEvent(marks, bids_eventsfname):
    print('Marks to add to tsv', marks)

    # %eliminar repetidos si hubiera
    # umrks = {};
    # while ~isempty(info)
    #     ii = find(all(ismember(info, info(1,:)),2));
    #     umrks = vertcat(umrks, info(1,:));
    #     info(ii,:) = [];
    # end
    # info = umrks;
    # for k=1:size(info,1)
    #     for h=1:size(info,2)
    #         if isempty(info{k,h}), info{k,h} = 'n/a'; end
    #     end
    # end
    # tab = {};
    # for k=1:size(info,1)
    #     info{k,5} = '1.0';
    #     tab{k,1} = [info{k,2} char(9) info{k,3} char(9) info{k,1} ...
    #         char(9) 'All' char(9) info{k,5} char(9) info{k,4}];
    # end

    # Create file if it doesn't exist
    fle = Path(bids_eventsfname)
    fle.touch(exist_ok=True)

    # Read TSV file
    tsv_read = pd.read_csv(bids_eventsfname, sep='\t')

    headers = ['onset', 'duration', 'annotation_type', 'channel', 'confidence', 'Annotator']


    for key in headers:
        if key not in tsv_read.columns:
            tsv_read[key] = 'n/a'

    with open(bids_eventsfname,'w') as write_tsv:
        write_tsv.write(tsv_read.to_csv(sep='\t', index=False))

    # Create accompanying JSON file
    fjson = bids_eventsfname.replace('.tsv', '.json')
    jsonUtils.createEvent(fjson)



