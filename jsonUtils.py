import json;

def createEvent(fjson):
     with open(fjson,'r+') as file:

        # First we load existing data into a dict.
        file_data = json.load(file)

        # Add new info
        if 'onset' not in file_data:
            file_data['onset'] = {}

        if 'duration' not in file_data:
            file_data['duration'] = {}

        if 'annotation_type' not in file_data:
            file_data['annotation_type'] = {}

        if 'HED' not in file_data['annotation_type']:
            file_data['annotation_type']['HED'] = {}

        if 'Levels' not in file_data['annotation_type']:
            file_data['annotation_type']['Levels'] = {}

        if 'channel' not in file_data:
            file_data['channel'] = {}

        file_data['onset']['Description'] = 'REQUIRED. Onset (in seconds) of the event, measured from the beginning of the acquisition of the first data point stored in the corresponding task data file. Negative onsets are allowed, to account for events that occur prior to the first stored data point.'
        file_data['duration']['Description'] = 'REQUIRED. Duration of the event (measured from onset) in seconds'
        file_data['annotation_type']['LongName'] = 'Hierarchical Event Descriptors annotations'
        file_data['annotation_type']['Description'] = 'EEG interpretation Hierarchical Event Descriptors annotations'
        file_data['annotation_type']['Levels']['eyem'] = 'A spike-like waveform created during patient eye movement. This artifact is usually found on all of the frontal polar electrodes with occasional echoing on the frontal electrodes'
        file_data['annotation_type']['Levels']['elec'] = 'An electrode artifact encompasses various electrode related artifacts. Electrode pop is an artifact characterized by channels using the same electrode with an electrographic phase reversal'
        file_data['annotation_type']['Levels']['musc'] = 'Muscle artifact. A very common, high frequency, sharp artifact that corresponds with agitation or nervousness in a patient.'
        file_data['annotation_type']['HED']['eyem'] = 'Eye-movement-horizontal-artifact'
        file_data['annotation_type']['HED']['elec'] = 'Electrode-pops-artifact'
        file_data['annotation_type']['HED']['musc'] = 'EMG-artifact'
        file_data['annotation_type']['HED']['eyem_musc'] = '(Eye-movement-horizontal-artifact , EMG-artifact)'
        file_data['annotation_type']['HED']['musc_elec'] = '( EMG-artifact , Electrode-pops-artifact )'
        file_data['annotation_type']['HED']['chew'] = 'Chewing-artifact'
        file_data['annotation_type']['HED']['shiv'] = 'Movement-artifact' # Bosch
        file_data['annotation_type']['HED']['eyem_shiv'] = '( Eye-movement-horizontal-artifact , Movement-artifact )' # Bosch
        file_data['annotation_type']['HED']['elpp'] = 'Electrode-pops-artifact'
        file_data['annotation_type']['HED']['eyem_elec'] = '( Eye-movement-horizontal-artifact , Electrode-pops-artifact )'
        file_data['annotation_type']['HED']['shiv_elec'] = '( Movement-artifact , Electrode-pops-artifact )'# Bosch
        file_data['annotation_type']['HED']['bckg'] = 'Non-biological-artifact' # Bosch
        file_data['annotation_type']['HED']['null'] = 'Undefined annotation' # Bosch
        file_data['channel']['LongName'] = 'Annotated channel'
        file_data['channel']['Description'] = 'List annotated channel. NA for all channels'

        # Sets file's current position at offset.
        file.seek(0)

        # convert back to json.
        json.dump(file_data, file, indent = 4)