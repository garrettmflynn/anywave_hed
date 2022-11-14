import anywave, sys

import mrkToEvents

print('Starting plugin... (anywave_hed)')
anywave.init(sys.argv)

properties = anywave.get_props()
filePath =  properties['bids_file_path']
const data = mrkToEvents.convert(filePath)

print(data)

# # assign valid tags from the HED-SCORE library
# scoreTags = ['seizure', 'EI' ] # TODO: Replace this with the actual list
# cfg = {
#     'labels': scoreTags
# }

# # get specified markers from the current AnyWave BIDS dataset
# filteredmarkers = anywave.get_markers(cfg)

# if filteredmarkers:
#     print('got filtered!')
#     print(filteredmarkers)

# else:
#     print('no markers with the following labels:', scoreTags)
#     markers = anywave.get_markers()
#     print('showing all markers', markers)

# # TODO: Add these markers to the BIDS dataset
