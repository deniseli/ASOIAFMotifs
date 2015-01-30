# Counts the single word occurences in each POV for each book and stores their
# ratio to the total occurences, with some filtering to get rid of uncommon
# words.

import os
import pickle
import string

def save_obj(obj, loc):
    with open('bigrams/'+ loc + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def remove_comma(word):
    if len(word) == 0:
        return word
    if word[-1] == ',':
        return word[:-1]
    return word

# Gets names of directories for each book
dirs = []
for filename in os.listdir("books"):
    dirs.append(filename[:-4] + "/")

for dir in dirs:
    all_counts = {}
    # Get all the file names containing POV titles in this directory
    fnames = []
    for filename in os.listdir("povs/" + dir):
        fnames.append(filename)
    # Remove the first file, .DS_STORE, from the list
    fnames = fnames[1:]
    for fname in fnames:
        print dir
        print fname
        # Do count for this file
        with open("povs/" + dir + fname) as f:
            text = f.readlines()[0]
        words = text.split(" ")
        counts = {}
        for i in range(len(words) - 1):
            a = remove_comma(words[i])
            b = remove_comma(words[i + 1])
            if len(a) == 0 or len(b) == 0:
                continue
            # Skip ends of sentences
            if a[-1] in string.punctuation:
                continue
            if b[-1] in string.punctuation:
                b = b[:-1]
            # Increment counter
            if a not in counts.keys():
                counts[a] = {}
            if b not in counts[a].keys():
                counts[a][b] = 0
            if a not in all_counts.keys():
                all_counts[a] = {}
            if b not in all_counts[a].keys():
                all_counts[a][b] = 0
            counts[a][b] += 1
            all_counts[a][b] += 1
        # Save bigram counts
        save_obj(counts, dir + fname[:-4])
    print dir
    print "All"
    save_obj(all_counts, dir + "All")
