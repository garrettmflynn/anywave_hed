
from pathlib import Path;
import pandas as pd;
import jsonUtils
import numpy as np
import math

def createEvent(marks, bids_eventsfname, annotator = 'n/a'):

    # Remove duplicates
    seen = set()
    def unique_generator(lst):
        for item in lst:
            tupled = tuple(item)
            if tupled not in seen:
                seen.add(tupled)
                yield item
    marks = list(unique_generator(marks))


    # Create file if it doesn't exist
    fle = Path(bids_eventsfname)
    fle.touch(exist_ok=True)

    # Read TSV file
    tsv_read = pd.read_csv(bids_eventsfname, sep='\t')

    headers = ['onset', 'duration', 'annotation_type', 'channel', 'confidence', 'Annotator']

    for key in headers:
        if key not in tsv_read.columns:
            tsv_read[key] = 'n/a'

    # Replace empty values with n/a
    tsv_read.fillna('n/a', inplace=True)


    order = ['annotation_type', 'onset', 'duration']
    newRow = {'channel': 'All', 'confidence': '1', 'Annotator': annotator}
    for line in marks:
        for i, key in enumerate(order):
            newRow[key] = line[i]

        comparisons = False
        for i, key in enumerate(order):
            print(key, tsv_read[key], newRow[key])
            value = type(tsv_read[key][0])(newRow[key])
            newComparison = (value == tsv_read[key]) & tsv_read['Annotator'] ## Must be from the conversion that includes an annotator...
            if (comparisons): comparisons *= newComparison.array
            else: comparisons = newComparison.array

        # Only add unique rows
        if not comparisons.any():
            tsv_read = tsv_read.append(newRow, ignore_index = True)


    with open(bids_eventsfname,'w') as write_tsv:
        write_tsv.write(tsv_read.to_csv(sep='\t', index=False))

    return tsv_read



