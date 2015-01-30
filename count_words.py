# Counts the single word occurences in each POV for each book and stores their
# ratio to the total occurences, with some filtering to get rid of uncommon
# words.

import os
import pickle
import re
from collections import Counter

def save_obj(obj, loc):
    with open('singleCounts/'+ loc + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

# Gets names of directories for each book
dirs = []
for filename in os.listdir("books"):
    dirs.append(filename[:-4] + "/")

all_counts = {}
for dir in dirs:
    total = Counter({})
    # Get all the file names containing POV titles in this directory
    fnames = []
    for filename in os.listdir("povs/" + dir):
        fnames.append(filename)
    # Remove the first file, .DS_STORE, from the list
    fnames = fnames[1:]
    for fname in fnames:
        # Do count for this file
        with open("povs/" + dir + fname) as f:
            text = f.readlines()[0]
        clean = re.sub(r'([^\'\s\w]|_)+', '', text)
        counts = Counter(clean.split(" "))
        all_counts[fname[:-4]] = counts
        total += counts
    save_obj(total, dir + "All")

    for name in all_counts.keys():
        counts = all_counts[name]
        relcounts = Counter({})
        for word in counts.keys():
            # We only want to consider ratios for words that appear more than 10
            # times and at least three times in this POV
            if total[word] >= 10 and counts[word] >= 3:
                relcounts[word] = 1.0 * counts[word] / total[word]
        save_obj(relcounts, dir + name)
