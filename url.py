#! /usr/bin/python

# This fixes the directories for running labs on the CS10 website
# This script is largely a terrible hack and shouldn't be used for long.

import os
import fnmatch
def findReplace(directory, find, replace, filePattern):
    for path, dirs, files in os.walk(os.path.abspath(directory)):
        for filename in fnmatch.filter(files, filePattern):
            filepath = os.path.join(path, filename)
            with open(filepath) as f:
                s = f.read()
            s = s.replace(find, replace)
            with open(filepath, "w") as f:
                f.write(s)

labs="/home/ff/cs10/public_html/bjc-r"
michael="/Volumes/Michael/Users/Michael/Dropbox/Projects/bjc-r copy"
findReplace(labs, "/bjc-r", "/~cs10/bjc-r", "*.html")
findReplace(labs, "/bjc-r", "/~cs10/bjc-r", "*.topic")
findReplace(labs, "/bjc-r", "/~cs10/bjc-r", "*.js")

