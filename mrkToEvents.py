import os;
import sys;

from pathlib import Path;

import tsvUtils
import mrkUtils
import artfUtils

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


    automatedAnnotatorName = 'AUTOMATED'
    

    bids_eventsfname =  edfFilePath.replace('_eeg.edf', '_events.tsv')
    anywaveAnnotationsDir = os.path.join(*base_dir, 'derivatives', 'anywave')
    autoannotations_path =  edfFilePath.replace('_eeg.edf', '_eeg.artf')
    autoMRKPath = os.path.join(anywaveAnnotationsDir, automatedAnnotatorName, sub, ses, type, filename.replace('_eeg.edf', '.mrk')) # get subject name and subject session

    # HANDLE AUTOMATIC ANNOTATIONS
    artfUtils.toMRK(autoannotations_path, autoMRKPath)

    # find all users who have made annotations
    # check existence of directory
    if not os.path.isdir(anywaveAnnotationsDir):
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

                # Augment automatic annotations with additional metadata
                if (f.name == automatedAnnotatorName): mrks = artfUtils.get(autoannotations_path)
                else: mrks = mrkUtils.read(mrkfile)                        

                marks = marks + mrks
                print("Transferred .mrk file for annotator", f.name)

            except Exception as e:
                print("Error: No .mrk file for annotator", f.name, e)
    
        finalData = tsvUtils.updateEvent(marks, bids_eventsfname, f.name)

    return finalData

# If run with command line argument
name = sys.argv[1]
if name: convert(name)