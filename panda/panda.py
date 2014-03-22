#! /usr/bin/env python3

import sys
import csv

scores = []
# TODO Parameter for Questions to drop, start and end
# Parameter for sorting.
if __name__ == '__main__':
    if not sys.argv[1]:
        print("No File Given")
        sys.exit(0)
    print("PANDA GRADER DROP SCORE CALCULATOR\n\n")
    gr = sys.argv[1]
    print(gr)
    grades = open(gr, "r")
    gr = csv.reader(grades)
    print("%36s |  %9s | %4s" % ("NAME", "SID", "DROP POINTS"))
    print('\t' + "-" * 54)
    for row in gr:
        # print(row)
        name = row[0]
        if name == "Name": # HEADER
            continue
        sid  = row[1]
        reading = row[6:16] # FIXME...
        scores.append((name, sid, min(reading)))
        print("%36s |  %9s | %4s" % (name, sid, min(reading)))
    print('\n\n\n\n')
    scores.sort(key=lambda i: i[0]) # Sort via name
    for s in scores:
        if float(s[2]) > 0:
            print("%36s |  %9s | %4s" % (s[0], s[1], s[2]))