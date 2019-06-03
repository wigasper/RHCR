import argparse

from PIL import Image, ImageDraw

def main():
    rect_coords = []

    with open("responses.tab", "r") as handle:
        for line in handle:
            line = line.split("\t")
            rect_coords.append([int(line[1]), int(line[2]), int(line[3]), int(line[4])])
    
    img = Image.open("0000051.png")
    draw = ImageDraw.Draw(img)

    for coord in rect_coords:
        draw.rectangle([coord[0], coord[1], coord[2], coord[3]], fill=None,
                        outline=0, width=3)
    
    img.save("box_test.png")

if __name__ == '__main__':
    main()