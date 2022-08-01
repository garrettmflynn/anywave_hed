import anywave, sys
anywave.init(sys.argv)
print('Starting AnyWave HED plugin!')
print(anywave.properties)  # output the content of a dict containing the global settings set by AnyWave for your plugin

# anywave.debug_connect(59000)  # note that this code can be run from anywhere you want in your Python dev environment.
# print('debug connected!')

# assign valid tags from the HED-SCORE library
scoreTags = ['seizure', 'EI' ]
cfg = {
    'labels': scoreTags
}

# get specified markers from the current AnyWave BIDS dataset
filteredmarkers = anywave.get_markers(cfg)

if filteredmarkers:
    print('got filtered!')
    print(filteredmarkers)

else:
    print('no markers with the following labels:', scoreTags)
    markers = anywave.get_markers()
    print('showing all markers', markers)



# TODO: Add these markers to the BIDS dataset
