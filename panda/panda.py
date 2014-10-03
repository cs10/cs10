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
    drop = 6
    if len(sys.argv) > 2:
        drop = int(float(sys.argv[2]))
    grades = open(gr, "r")
    gr = csv.reader(grades)
    print("%36s |  %9s | %4s" % ("NAME", "SID", "DROP"))
    print('\t' + "-" * 50)
    for row in gr:
        # print(row)
        # print(row[6:6 + drop])
        name = row[0]
        if name == "Name": # HEADER
            continue
        sid  = row[1]
        reading = row[6:(6 + drop + 2)] # FIXME...
        # Merge reading scores with two parts.
        # quest
        # 1: 2 parts, 2: 2 parts
        reading[0:2] = [ (float(reading[0]) + float(reading[1])) ]
        reading[1:3] = [ (float(reading[1]) + float(reading[2])) ]
        reading = list(map(float, reading))
        scores.append((name, sid, min(reading)))
        print("%36s |  %9s | %4s" % (name, sid, min(reading)))
    print('\n\n\n\t')
    print('SCORES NOT ZERO')
    scores.sort(key=lambda i: i[0]) # Sort via name
    for s in scores:
        if float(s[2]) > 0:
            print("%36s |  %9s | %4s" % (s[0], s[1], s[2]))