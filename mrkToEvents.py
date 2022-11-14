import os;
import sys;

from pathlib import Path;

import tsvUtils
import mrkUtils

def convert(edfFilePath):
    edfFilePath = os.path.normpath(edfFilePath)
    edfFilePath = os.path.relpath(edfFilePath, os.getcwd())

    try:
        *base_dir, sub, ses, type, filename = edfFilePath.split(os.sep)
        isub = sub.startswith('sub-')
        ises = ses.startswith('ses-')

    except Exception as e:
        print('This directory is not an EEG-BIDS structure')
        return None


    bids_eventsfname =  edfFilePath.replace('_eeg.edf', '_events.tsv')

    # find all users who have made annotations
    anywaveAnnotationsDir = os.path.join(*base_dir, 'derivatives', 'anywave')


    try:
        mrkUtils.read(anywaveAnnotationsDir)

    except IOError:
        print("Error: No annotations directory:", anywaveAnnotationsDir)

    p = Path(anywaveAnnotationsDir)

    finalData = False

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

        finalData = tsvUtils.createEvent(marks, bids_eventsfname, f.name)

    return finalData

# If run with command line argument
name = sys.argv[1]
if name: convert(name)