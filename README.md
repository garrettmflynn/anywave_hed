# anywave_hed
 An AnyWave plugin to place HED tags into the BIDS format

## Description
Currently, this plugin is a **test** Python plugin for the AnyWave annotation software. If running correctly, it should print messages to the console from Anywave.

We are in the process of creating a Python version of a working MATLAB plugin for converting .mrk to BIDS _events.tsv files.

## How to Install
> A Python plugin is a folder located in the user home dir.
> - **Windows:** Documents\AnyWave\Plugins\Python
> - **Linux:** /home/username/AnyWave/Plugins/Python
> - **MacOS:** /users/username/AnyWave/Plugins/Python

Once added to the correct folder, you can run this plugin under Processes/Markers/Save as HED Tags in BIDS

## Future Work
- Convert [anywave_mrk_to_events_tsv.m](./anywave_mrk_to_events_tsv.m) from MATLAB to Python, which will allow us to convert AnyWave's native .mrk annotation files to appropriate BIDS annotations.


## Notes
### Debug Mode
https://gitlab-dynamap.timone.univ-amu.fr/anywave/anywave/-/wikis/Py_debug

### Plugin Basics
https://gitlab-dynamap.timone.univ-amu.fr/anywave/anywave/-/wikis/Python_plugins