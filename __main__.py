import anywave, sys
anywave.init(sys.argv)
print('starting!')
print(anywave.properties)  # output the content of a dict containing the global settings set by AnyWave for your plugin
print(anywave.properties.data_path)

anywave.debug_connect(59000)  # note that this code can be run from anywhere you want in your Python dev environment.
print('debug connected!')

markers = anywave.get_markers()
print(markers)

print(markers)


cfg = []
cfg['labels'] = ['seizure', 'EI' ]
filteredmarkers = anywave.get_markers(cfg)
print(filteredmarkers)

if filteredmarkers:
    print('got filtered!')

