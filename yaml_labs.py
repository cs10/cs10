#! /usr/bin/env python3

import os


# TO BE RUN FROM INSIDE BJC-R DIRECTORY
LABS_DIR = "cur"

# YAML front matter for Jekyll
prepend = "---\n---\n\n"

def add_to_file(inp):
    print(inp)
    f = open(inp, "r")
    content = prepend
    try:
         content += f.read()
    except:
        content += str(f.read().encode('latin-1'))
    f.close()
    f = open(inp, "w")
    f.write(content)
    f.flush()
    f.close()

if __name__ == '__main__':
    paths = os.walk(LABS_DIR)
    for path, subdir, files in paths:
        for f in files:
            if ".html" in f:
                add_to_file(path + '/' + f)
