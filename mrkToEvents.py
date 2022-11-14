import os;
import sys;

from pathlib import Path;

import tsvUtils
import mrkUtils

def mrkToEvents(edfFilePath):

    try:
        *base_dir, sub, ses, type, filename = os.path.normpath(edfFilePath).split(os.sep)
        isub = sub.startswith('sub-')
        ises = ses.startswith('ses-')

    except Exception as e:
        print('This directory is not an EEG-BIDS structure')
        return None


    bids_eventsfname =  edfFilePath.replace('_eeg.edf', '_events.tsv')

    # find all users who have made annotations
    anywaveAnnotationsDir = os.path.join(*base_dir, 'derivatives', 'anywave')

    p = Path(anywaveAnnotationsDir)

    # All subdirectories in the current directory, not recursive.
    for f in filter(Path.is_dir, p.iterdir()):
        derivativesDir = os.path.join(anywaveAnnotationsDir, f.name, sub, ses, type) # get subject name and subject session

        def checkIfMRK(f): 
            return f.name.endswith('.mrk')


        marks = []
        derivativesDirPath = Path(derivativesDir)
        for mrkfile in filter(checkIfMRK, derivativesDirPath.iterdir()):

            try:
                mrks = mrkUtils.read(mrkfile)
                marks = marks + mrks
                print("Got .mrk file for annotator", f.name)

            except IOError:
                print("Error: No .mrk file for annotator", f.name)

        tsvUtils.createEvent(marks, bids_eventsfname, f.name)


# Run with command line argument
name = sys.argv[1]
mrkToEvents(name)