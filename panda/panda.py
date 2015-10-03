#! /usr/bin/env python3

import sys
import csv
from heapq import nsmallest

scores = []
# TODO Parameter for Questions to drop, start and end
# Parameter for sorting.
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error No File or drop count Given")
        print("Usage:\npanda.py FILE.CSV DROP-QUESTIONS [drop-number]")
        print("Drop Questions is the number of questions to count in dropping.")
        print("This current starts from 1 and goes to N.")
        print("Drop Number defaults to 1, otherwise should be an integer.")
        sys.exit(1)
    print("PANDA GRADER DROP SCORE CALCULATOR\n")
    file = sys.argv[1]
    print('\t' + file)
    DROP_Qs = 6
    if len(sys.argv) > 2:
        DROP_Qs = int(float(sys.argv[2]))
    TODROP = 1
    if len(sys.argv) > 3:
        TODROP = int(float(sys.argv[3]))
    grades = open(file, "r")
    grade_data = csv.reader(grades)
    print('\t' + "-" * 54)
    print("%36s |  %9s |  %10s | %8s" % ("NAME", "SID", "DROP SCORE", "INDIV Q SCORES"))
    print('\t' + "-" * 54)
    for row in grade_data:
        # print(row)
        name = row[0]
        if name == "Name": # HEADER
            print(row[7:7 + DROP_Qs]) # Verify the question titles
            continue
        sid  = row[1]
        reading = row[7:7 + DROP_Qs] # FIXME...
        # Merge reading scores with two parts.
        # quest
        # 1: 2 parts, 2: 2 parts
        # reading[0:2] = [ (float(reading[0]) + float(reading[1])) ]
        # reading[1:3] = [ (float(reading[1]) + float(reading[2])) ]
        reading = list(map(float, reading))
        minScores = nsmallest(TODROP, reading)
        dropScore = sum(minScores)
        scores.append((name, sid, dropScore, minScores))
        print("%36s |  %9s | %10s | %8s" % (name, sid, dropScore, minScores))
    print('\t' + ('=' * 54))
    print('\tSCORES NOT ZERO')
    scores.sort(key=lambda i: i[0]) # Sort via name
    for s in scores:
        if float(s[2]) > 0:
            print("%36s |  %9s | %10s | %8s" % (s[0], s[1], s[2], s[3]))