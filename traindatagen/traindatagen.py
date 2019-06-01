#!/usr/bin/env python3

import os
import sys
import time
import logging
import argparse
import traceback
from random import randint

from PIL import Image, ImageDraw, ImageFont
import numpy as np

def format_line(line, max_width=90):
    ''' Ensures that lines of text terminate reasonably even if document has no newlines '''
    line = line.split()
    while len(line) > 0:
        out = line[0]
        line = line[1:]
        while len(line) > 0 and len(out) + len(line[0]) + 1 < max_width:
            out = " ".join([out, line[0]])
            line = line[1:]
        yield out

def txt_to_cursive_img(doc, logger):
    ''' turns a document text into cursive images using the dictionary
        :params:
            doc- list of lines of text
            logger- log object
        :return:
            array of b&w images of cursive letters
    '''
    try:
        width = 2700
        height = 4000

        img = Image.new('L', (width, height), 255)
        draw = ImageDraw.Draw(img)

        fonts = os.listdir("./fonts")
        font = ImageFont.truetype(f"./fonts/{fonts[randint(0,2)]}", 120)

        current_height = 30
        for line in doc:
            text_w, text_h = draw.textsize(line, font=font)
            draw.text((30, current_height), line, font=font, fill=0)
            current_height = current_height + text_h + 15
        
        return img

    except Exception as e:
        traceback.print_exc()
        trace = traceback.format_exc()
        logger.error(repr(e))
        logger.critical(trace)
        raise
    
def main():
    doc = []
    
    # Get command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input file path", type=str, nargs=1)
    parser.add_argument("-o", "--output", help="output file path", type=str, nargs=1)
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
        in_path = args.input[0]
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
        out_path = args.output[0]
        if out_path.split(".")[-1] not in supported_formats:
            out_path = "".join([out_path, ".png"])
    else:
        out_path = in_path.split("/")[-1]
        out_path = "".join(out_path.split(".")[:-1])
        out_path = f"{out_path}.png"
    
    # Change each letter to a cursive image
    logger.info('converting string doc to cursive images')
    out = txt_to_cursive_img(doc, logger)
    
    out.save(f"{out_path}")
    logger.info(f"Translated {in_path} to {out_path}")
    
if __name__ == '__main__':
    main()