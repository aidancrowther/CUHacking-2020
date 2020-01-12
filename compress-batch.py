#!/usr/bin/python
from PIL import Image
import os, sys

path = "training/leedsbutterfly/images/"
dirs = os.listdir( path )

def resize():
    for item in dirs:
        if os.path.isfile(path+item):
            im = Image.open(path+item)
            f, e = os.path.splitext(path+item)
            print(path+item)
            imResize = im.resize((400,400), Image.ANTIALIAS)
            imResize.save(f + '.small.png', 'PNG', quality=90)

resize()