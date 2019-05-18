#!/usr/bin/env python3

import sys
import time
import logging
import argparse

from keras.preprocessing.image import load_img
import matplotlib.pyplot as plt
import numpy as np

# This is a quick and dirty formatting method to ensure that line widths
# are reasonable if input doc does not have newlines
# Adds words to lines until the next word would put it over the max width
# Then yields the line
def format_line(line, max_width=90):
    line = line.split()
    while len(line) > 0:
        out = line[0]
        line = line[1:]
        while len(line) > 0 and len(out) + len(line[0]) + 1 < max_width:
            out = " ".join([out, line[0]])
            line = line[1:]
        yield out

class traindatagen:
    
    def main():
        doc = []
        
        # Get command line args
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--input", help="input file path")
        parser.add_argument("-o", "--output", help="output file path")
        args = parser.parse_args()
        
        # Set up logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler("traindatagen.log")
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Output formats supported by matplotlib
        supported_formats = ["eps", "jpeg", "jpg", "pdf", "pgf", "png", "ps", 
                             "raw", "rgba", "svg", "svgz", "tif", "tiff"]
            
        if args.input:
            in_path = args.input
            # Read in document to transform to cursive
            with open(in_path, "r") as handle:
                for line in handle:
                    for frmtd_line in format_line(line):
                        doc.append(frmtd_line)
        else:
            in_path = "sys.stdin"
            # haven't tested sys.sdtin usage
            for line in sys.stdin.read():
                for frmtd_line in format_line(line):
                    doc.append(frmtd_line)
        
        if args.output:
            out_path = args.output
            if out_path.split(".")[-1] not in supported_formats:
                out_path = "".join([out_path, ".png"])
        else:
            out_path = f"{in_path.split("/")[-1].split(".")[:-1]}.png"
            
        #########################################
        # for testing in IDE, read in doc:
#        with open("./traindatagen/cyrillic.3.test", "r") as handle:
#                for line in handle:
#                    for frmtd_line in format_line(line):
#                        doc.append(frmtd_line)
        #########################################
        
        # Build dict
        letters_dict = {}
        with open("letters.dict", "r") as handle:
            for line in handle:
                line = line.strip("\n").split(",")
                letters_dict[line[0]] = line[1]
        
        for letter in letters_dict:
            fp =f"letters/{letters_dict[letter]}.png"
            letters_dict[letter] = np.array(load_img(fp, color_mode="grayscale"))
        
        # Whitespace, should make this variable for inconsistent spacing
        letters_dict[' '] = np.ones((127,40)) * 255
        
        # Change each letter to a cursive image
        out = []
        for line in doc:
            line_out = []
            for letter in line:
                try:
                    line_out.append(letters_dict[letter])
                except KeyError:
                    logger.error(f"Symbol {letter} not in dict")
            out.append(np.hstack(tuple(line_out)))

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
        
        plt.imsave(f"{out_path}", out, cmap='gray')
        logger.info(f"Translated {in_path} to {out_path}")
        
    if __name__ == '__main__':
        main()