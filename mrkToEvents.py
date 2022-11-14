import os;
import sys;

import tsvUtils
import mrkUtils

def mrkToEvents(edfFilePath):

    try:
        *path, sub, ses, type, filename = os.path.normpath(edfFilePath).split(os.sep)
        print(path, sub, ses, type, filename)
        isub = sub.startswith('sub-')
        ises = ses.startswith('ses-')
        base_dir = os.path.join(*path, sub, ses, type)
        print(base_dir)

    except Exception as e:
        print('This directory is not an EEG-BIDS structure')
        print(e)
        return None


    bids_eventsfname =  edfFilePath.replace('_eeg.edf', '_events.tsv')

    # find all users who have made annotations
    # if (os.listdir(base_dir).len != 0) & (base_dir[-1] != os.sep):
    #     base_dir = [base_dir  filesep];

    anywaveAnnotationsDir = os.path.join(base_dir, 'derivatives', 'anywave')
    print(anywaveAnnotationsDir)
    # alld = dir([anywaveAnnotationsDir '*.*'])
    # ii = find([alld.isdir])
    # alld = alld(ii)
    # nm = {alld.name}
    # ii = find(ismember(nm, '.'))
    # nm(ii) = []
    # alld(ii) = []
    # ii = find(ismember(nm, '..'))
    # nm(ii) = []
    # alld(ii) = []
    # # get subject name and subject session
    marks = []
    # for k=1:length(alld):
    #     dn = [anywave_annotations_dir alld(k).name filesep sub_name filesep ses_name filesep];
    #     if exist([dn 'eeg'], 'dir')
    #         dn = [dn 'eeg' filesep];

    #     fx = dir([dn '*.mrk']);
    #     for h=1:length(fx):
    #         mrks = mrkUtils.read([dn fx(h).name]);
    #         mrks = horzcat(mrks, repmat({alld(k).name}, size(mrks,1), 1));
    #         marks = vertcat(marks, mrks);

    tsvUtils.createEvent(marks, bids_eventsfname)



# Run with command line argument
name = sys.argv[1]
mrkToEvents(name)