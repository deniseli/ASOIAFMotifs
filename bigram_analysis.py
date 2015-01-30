# Counts the single word occurences in each POV for each book and stores their
# ratio to the total occurences, with some filtering to get rid of uncommon
# words.

import os
import pickle

def load_obj(loc):
    with open(loc + '.pkl', 'rb') as f:
        return pickle.load(f)

# Gets names of directories for each book
dirs = []
for filename in os.listdir("books"):
    dirs.append(filename[:-4] + "/")

for dir in dirs:
    # Load bigram counts for All POVs and count totals for each first word
    counts = load_obj('bigrams/' + dir + 'All')
    all = {}
    for word in counts.keys():
        total = 0
        for x in counts[word].keys():
            total += counts[word][x]
        for x in counts[word].keys():
            all[(word, x)] = 1.0 * counts[word][x] / total
    # Get all the file names containing POV titles in this directory
    fnames = []
    for filename in os.listdir("povs/" + dir):
        fnames.append(filename)
    # Remove the first file, .DS_STORE, from the list
    fnames = fnames[1:]
    for fname in fnames:
        # Load POV chapters
        with open("povs/" + dir + fname) as f:
          pov_text = f.readlines()[0]
        # Load bigram counts for each POV and calculate totals
        pov_ratios = []
        counts = load_obj('bigrams/' + dir + fname[:-4])
        for word in counts.keys():
            total = 0
            for x in counts[word].keys():
                total += counts[word][x]
            for x in counts[word].keys():
                if total >= 10 and counts[word][x] >= 3:
                    freq = 1.0 * counts[word][x] / total
                    pov_ratios.append((word, x, freq / all[(word, x)]))
        pov_ratios = sorted(pov_ratios, key=lambda x: x[2], reverse=True)
        # Find the motifs!
        motifs = []
        for start in pov_ratios:
            if start[2] < 1.5: break
            maybe_motifs = [[start[0], start[1]]]
            while len(maybe_motifs) > 0:
                curr = maybe_motifs.pop(0)
                matching = [x for x in pov_ratios if x[0] == curr[-1] and x[2] > 1.5]
                if len(matching) > 2:
                    matching = matching[:2]
                matched = False
                for match in matching:
                    if pov_text.find(' '.join(curr + [match[1]])) != -1:
                        matched = True
                        maybe_motifs.append(curr + [match[1]])
                if not matched and len(curr) >= 4:
                    motifs.append(' '.join(curr))
        # Remove contained motifs
        clean_motifs = []
        for i in range(len(motifs)):
            contained = False
            for j in range(len(motifs)):
                if motifs[j].find(motifs[i]) != -1 and i != j:
                    contained = True
                    break
            if not contained:
                clean_motifs.append(motifs[i])
        print dir[:-1]
        print fname[:-4]
        print clean_motifs
