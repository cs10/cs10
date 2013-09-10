#! /usr/bin/env python3

# For fixing the images in the labs repo
# Walk the labs directory for HTML files
# Find an <img tag
# The read th image file from src and get dimensions
# Write width and height back to the file

import os

from PIL import Image

labs = "~/Dropbox/Projects/bjc-r"
findStr = "<img\s+([src|width|height|hspace]=\".*\")+\s*/>"
writeStr = "<img src=\"{0}\" width=\"{1}\" height=\"{2}\" />"

def process(path, directory, file):
    # Get file and do a find using findStr
    
    imgSrc = "" # src group of the find regex
    os.chdir("") # go to the proper place
    img = Image.open(imgSrc)
    # get the image's width and height in pixels
    w, h = img.size
    replace = writeStr.format(imgSrc, w, h)
    # Replace the <img /> with the replace string

for (path, dirname, filename) in os.walkdir(labs):
    if filename.endswith(".html"):
        process(path, dirname, filename)