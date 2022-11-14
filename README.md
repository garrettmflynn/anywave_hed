# anywave_hed
 An AnyWave plugin to place HED tags into the BIDS format

## Description
This plugin converts AnyWave's native .mrk files to BIDS _events.tsv files after closing the program.

## How to Install
> A Python plugin is a folder located in the user home dir.
> - **Windows:** Documents\AnyWave\Plugins\Python
> - **Linux:** /home/username/AnyWave/Plugins/Python
> - **MacOS:** /users/username/AnyWave/Plugins/Python

Once added to the correct folder, the plugin will show up under the Processes/Markers/Save as HED Tags in BIDS.

### Creating and Linking a Virtual Environment
1. Create the virtual environment
```
Python3 -m venv  c:\dev\venv\anywave
```

2. Activate the virtual environment
```
c:\dev\venv\anywave\Scripts\activate
```

3. Install the AnyWave Plugin API to the environment
```
pip install anywave-plugin-api
```

4. Link the virtual environment in the AnyWave preferences

## Notes
### Debug Mode
https://gitlab-dynamap.timone.univ-amu.fr/anywave/anywave/-/wikis/Py_debug

### Plugin Basics
https://gitlab-dynamap.timone.univ-amu.fr/anywave/anywave/-/wikis/Python_plugins