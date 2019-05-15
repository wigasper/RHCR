#!/usr/bin/env python3

import sys
import getopt

from keras.preprocessing.image import load_img
import matplotlib.pyplot as plt
import numpy as np

# This is a quick and dirty formatting method to ensure that line widths
# are reasonable if input doc does not have newlines
# Adds words to lines until the next word would put it over the max width
# Then yields the line
def format_line(line, max_width=120):
    line = line.split()
    while len(line) > 0:
        out = line[0]
        line = line[1:]
        while len(line) > 0 and len(out) + len(line[0]) + 1 < max_width:
            out = " ".join([out, line[0]])
            line = line[1:]
        yield out


def usage():
    print("\nUsage: ", sys.argv[0], " \n")

class traindatagen:
    
    def main():
        options = {}
        doc = []
        
        try:
            opts, args = getopt.getopt(sys.argv[1:], "i:")
        
        except getopt.GetoptError as err:
            sys.stdout = sys.stderr

            print(str(err))

            usage()

            sys.exit(2)
            
        for (opt, arg) in opts:
            options[opt] = arg
            
        if "-i" in options.keys():
            # Read in document to transform to cursive
            with open(options["-i"], "r") as handle:
                for line in handle:
                    for frmtd_line in format_line(line):
                        doc.append(frmtd_line)
        else:
            # haven't tested sys.sdtin usage
            for line in sys.stdin.read():
                for frmtd_line in format_line(line):
                    doc.append(frmtd_line)

        #########################################
        # for testing in IDE, read in doc:
#        with open("./traindatagen/cyrillic.3.test", "r") as handle:
#                for line in handle:
#                    for frmtd_line in format_line(line):
#                        doc.append(frmtd_line)
        #########################################
        
        # Build dict
        letters_dict = {}
        with open("./traindatagen/letters.dict", "r") as handle:
            for line in handle:
                line = line.strip("\n").split(",")
                letters_dict[line[0]] = line[1]
        
        for letter in letters_dict:
            fp ="./traindatagen/letters/{}.png".format(letters_dict[letter])
            letters_dict[letter] = np.array(load_img(fp, color_mode="grayscale"))
        
        # Whitespace, should make this variable for inconsistent spacing
        letters_dict[' '] = np.ones((127,40)) * 255
        
        # Change each letter to a cursive image
        out = []
        for line in doc:
            ###########
            # Remove conditional here once we have all letters!!!!!!!
            line = [letters_dict[letter] for letter in line if letter in letters_dict.keys()]
            out.append(np.hstack(tuple(line)))

        # Get max width
        width = max([line.shape[1] for line in out])
        
        # Pad all lines to max width
        index = 0
        for line in out:
            if line.shape[1] < width:
                pad = np.ones((line.shape[0], (width - line.shape[1]))) * 255
                out[index] = np.hstack((line, pad))
            index += 1

        # Combine vertically
        out = np.vstack(tuple(out))
        
        plt.imsave("./traindatagen/test.jpg", out, cmap='gray')
        
    if __name__ == '__main__':
        main()