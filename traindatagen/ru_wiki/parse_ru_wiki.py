#!/usr/bin/env python3

valid_letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "
        
test = []

with open("ruwiki.test", "r") as fp:
    for line in fp:
        line_out = ""
        for char in line:
            if char in valid_letters:
                line_out = "".join([line_out, char])
        line_out = " ".join(line_out.split())
        if line_out:        
            test.append(line_out)
