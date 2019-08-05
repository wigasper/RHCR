import argparse
from PIL import Image, ImageDraw

def box_drawer(imageFile, targetsFile, outFile):
    '''takes the saved letter selection boxes (defined in the targetsFile) 
    and draws them over the imageFile for human visual inspection'''
    rect_coords = []

    with open(targetsFile, "r") as handle:
        for line in handle:
            line = line.split("\t")
            rect_coords.append([int(line[1]), int(line[2]), int(line[3]), int(line[4])])
    
    img = Image.open(imageFile)
    draw = ImageDraw.Draw(img)

    for coord in rect_coords:
        draw.rectangle([coord[0], coord[1], coord[2], coord[3]], fill=None,
                        outline=0, width=3)

    img.save(outFile)

def getArgs():
    ''' used to get command-line arguments when run standalone '''
    parser = argparse.ArgumentParser(description='draws bounding boxes from target file over image for human inspection')
    parser.add_argument('imageFile', type=str, help='image to draw boxes over')
    parser.add_argument('targetsFile', type=str, help='file with box coords, in standard format defined in repo README')
    parser.add_argument('outFile', type=str, help='output image file, suggested format is .png')
    return parser.parse_args()

if __name__ == '__main__':
    args = getArgs()