#!/usr/bin/env python3
from random import random

def random_punctuator(word):
    if random() < .08:
        return "".join([word, ","])
    if random() < .066:
        return "".join([word, "."])
    if random() < .02:
        return "".join([word, "?"])
    if random() < .04:
        if random() < .51:
            return "".join([word, '"'])
        else:
            return "".join(['"', word])
    return word

def format_line(line, max_width=50):
    line = line.split()
    while len(line) > 0:
        out = random_punctuator(line[0])
        line = line[1:]
        while len(line) > 0 and len(out) + len(line[0]) + 1 < max_width:
            out = " ".join([out, random_punctuator(line[0])])
            line = line[1:]
        yield out

valid_letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "

identifier = 0
out = ""

with open("ruwiki.test", "r") as fp:
    for line in fp:
        if len(out) > 990:
            with open(f"./generated_text/{str(identifier).zfill(7)}.txt", "w") as fp:
                for out_line in format_line(out):
                    fp.write("".join([out_line, "\n"]))
            identifier += 1
            out = ""
        line_out = ""
        for char in line:
            if char in valid_letters:
                line_out = "".join([line_out, char])
        line_out = " ".join(line_out.split())
        if line_out:        
            out = " ".join([out, line_out])
