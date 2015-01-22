# This script takes the complete texts of ASOIAF and splits them into separate
# files by chapter POV. These are each split by book.

import os

def is_title(line):
    return line.isupper() and \
        len(line) > 2 and \
        all(x.isalpha() or x.isspace() for x in line)

fnames = []
for filename in os.listdir("books"):
    fnames.append(filename)

fcontents = []
for fname in fnames:
    with open("books/" + fname) as f:
        fcontents.append(f.readlines())

currPOV = ""
currFile = None
currContents = ""
for i in range(len(fcontents)):
    for l in fcontents[i]:
        line = l.rstrip('\n')
        if line == "MEANWHILE, BACK ON THE WALL...":
            # The last chapter in Book 4 is SAMWELL, which is followed by a
            # short note from GRRM, followed by the Appendix. The first line of
            # this non-book part of the book beings with "MEANWHILE, BACK ON THE
            # WALL", so this check cuts everything after that from the processed
            # POV files.
            break
        if is_title(line):
            # This line denotes the start of a new chapter. If a file for this
            # character already exists, append to that file. Otherwise, create a new
            # file for this character in the appropriate directory.
            # Flush the contents of currContents to the appropriate file
            if len(currContents) > 0:
                filename = "povs/"+ fnames[i][:-4] + "/" + \
                    currPOV.title().replace(" ", "") + ".txt"
                with open(filename, "a") as f:
                    f.write(currContents + " ")
            # Update currPOV
            currPOV = line
            # Clear currContents
            currContents = ""
        else:
            # This line is part of a chapter. Clean the text and append it to
            # currContents.
            clean = line.rstrip(' ').lower()
            clean = clean.replace('"', '').replace("  ", " ").replace(" '", "'")
            if len(clean) > 0:
                if len(currContents) > 0:
                    currContents += " "
                currContents += clean
    # We have reached the end of a book. Flush the contents remaining in
    # currContents to the appropriate POV file.
    filename = "povs/"+ fnames[i][:-4] + "/" + \
        currPOV.title().replace(" ", "") + ".txt"
    with open(filename, "a") as f:
        f.write(currContents)
