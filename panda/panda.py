#! /usr/bin/env python3

import sys
import csv
from heapq import nsmallest

# TODO: finish cleanup...
def dropRow(name, sid, totalDrop, dropValues):
    return (name, sid, totalDrop, dropValues)

def sortAndPrint(data):
    data.sort(key=lambda i: i[0]) # Sort via name
    data = [item for item in data if float(item[2]) > 0]
    for student in data: print(FORMATTER % student)

# TODO: extract logic into this function.
def createDropTable(csvData):
    pass

FORMATTER = "%36s |  %10s |  %10s | %10s"
HEADERS   = ("NAME", "SID", "DROP SCORE", "INDIV Q SCORES")
DASHES    = "\t" + "-" * 70
EQUALS    = '\t' + '=' * 70

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
    print("PANDA GRADER DROP SCORE CALCULATOR")
    file = sys.argv[1]
    # print('\t' + file)
    DROP_Qs = 6
    if len(sys.argv) > 2:
        DROP_Qs = int(float(sys.argv[2]))
    TODROP = 1
    if len(sys.argv) > 3:
        TODROP = int(float(sys.argv[3]))
    grades = open(file, "r")
    grade_data = csv.reader(grades)
    # TODO: This should at least be a function....
    for row in grade_data:
        # print(row)
        name = row[0]
        sid  = row[1]
        if sid == "SID": # HEADER
            print('Questions Confirmation:', end='\n\t')
            print(row[6:6 + DROP_Qs]) # Verify the question titles
            print(DASHES)
            print(FORMATTER % HEADERS)
            print(DASHES)
            continue
        reading = row[6:6 + DROP_Qs] # FIXME...
        # TODO: This should be a function call.
        # Merge reading scores with two parts.
        # reading[0:2] = [ (float(reading[0]) + float(reading[1])) ]
        # reading[1:3] = [ (float(reading[1]) + float(reading[2])) ]
        reading = list(map(float, reading))
        minScores = nsmallest(TODROP, reading)
        dropScore = sum(minScores)
        info = (name, sid, dropScore, minScores)
        scores.append(info)
        print(FORMATTER % info)
    print(EQUALS)
    print('\n\tSCORES NOT ZERO\n')
    sortAndPrint(scores)
