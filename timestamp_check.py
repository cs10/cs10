### Handles timestamp checking for CS10 assignments.
### Updated: September 12, 2013
###
### Run using:    python timestamp_check.py [duedate] [--noadjust] [--timeonly] [--nosubonly] [--summary] [--dst] [--nodst]
### where the optional duedate argument should be of the form [YYYY]MMDDHHMM
###    ([year,] month, day, hour, minute) (using military time), and where adding the:
### --noadjust flag tells the program not to adjust timestamps to Pacific Standard Time.
### --timeonly flag suppresses the output of "no submission".
### --nosubonly flag suppresses the output of late submissions.
### --summary flag suppresses all output, except for a summary of the results.
### --dst flag specifies that the location is currently in Daylight Saving Time.
### --nodst flag specifies that the location is not currently in Daylight Saving Time.
### If no additional arguments are given, all timestamps will be dumped to the terminal.
### timestamp_check.py file should be placed in the directory containing all submissions,
### and can be run using either python 2 or 3.
###
### Example (from HW2, spring 2013): python timestamp_check.py 02152359
### (due date == February 15 @ 11:59 PM)
###
### @author Peter Sujan
### Bugs or questions: peterasujan@gmail.com

from os import listdir
from os import chdir
from datetime import datetime
from datetime import timedelta
from re import match
from sys import argv

class Timestamp(object):
    """ Represents a timestamp. """

    def __init__(self, text, adjust, dst):
        if len(text) == 8:
            self._year = datetime.now().year
            self._month = int(text[0:2])
            self._day = int(text[2:4])
            self._hour = int(text[4:6])
            self._minute = int(text[6:8])
        else:
            self._year = int(text[0:4])
            self._month = int(text[4:6])
            self._day = int(text[6:8])
            self._hour = int(text[8:10])
            self._minute = int(text[10:12])
                
        self._dst = dst
        self._date = datetime(self._year, self._month, self._day, self._hour, self._minute)
        self._date -= timedelta(hours=adjust * self.GMTOffset())
        
        
    def __str__(self):
        return self._date.__str__()[:-3]
        
    def getdate(self):
        return self._date
        
    def late(self, dueDate):
        """ Returns True iff this timestamp is late relative to dueDate. """
        return self._date > dueDate.getdate()

    def slipdays(self, dueDate):
        if self.late(dueDate):
            return (self._date - dueDate.getdate()).days + 1
        return 0
        
    def GMTOffset(self):
        offset = -8
        if self._dst == None:
            try:
                beginning = datetime(self._year, DST_START[self._year][0], DST_START[self._year][0], 2, 0)
                end = datetime(self._year, DST_END[self._year][0], DST_END[self._year][1], 2, 0)
            except KeyError:
                print(("\nError: It appears that there is no DST information entered for the year specified({0}).\n"
                       + "Please go to http://www.timeanddate.com/ and update the variables DST_START and\n"
                       + "DST_END to reflect the current year's DST schedule.\n"
                       + "Alternatively, you may manually specify the current status of daylight savings\n"
                       + "using the --dst or --nodst flag.\n").format(self._year))
                exit()

            if (self._date > beginning and self._date < end):
                offset += 1
        elif dst:
            offset += 1
        return offset


def output(adjust, duedate, sub, print_late, dst):
    total = 0
    late = 0
    nosub = 0
    if duedate:
        due = Timestamp(duedate, False, None)
        print("\nChecking due date: ")
        print(due)
        if adjust:
            print("(timestamps are printed after being adjusted)")
    else:
        print("No timestamp given. All submissions will be printed.")
    folders = listdir(".")
    print("\n")
    for folder in folders:
        if folder.find(".") == -1:
            chdir(folder)
            try:
                f = open("timestamp.txt")
                text = f.readline()
                stamp = Timestamp(text, adjust, dst)
                if not duedate and print_late:
                    print(folder)
                    print(stamp)
                    print("\n")
                elif duedate and stamp.late(due):
                    if print_late:
                        print(folder)
                        print(stamp)
                        print("days late: {0}".format(stamp.slipdays(due)))
                        print("\n")
                    late += 1
                f.close()
            except IOError:
                if sub:
                    print(folder)
                    print("No Submission\n")
                nosub += 1
            total += 1
            chdir("..")
    
    print("{0} submissions were processed.".format(total))
    print("{0} were late and {1} contained no submission.".format(late, nosub))
    print("done")

def argv_find(args, string):
    """ True iff string (can be a regular expression) is present in args. """
    for item in args:
        if match(string, item):    
            return item
    return False

def get_value(string):
    return string[string.index("="):]

### constants for handling Daylight Saving Time.
### Note that these are for the United States, and were updated on 9/11/2013.
### DST dates are subject to change.

DST_START = {2013:(3, 10),
             2014:(3, 9)}

DST_END = {2013:(11, 3),
           2014:(11, 2)}


### main program           
adjust = not argv_find(argv, "--noadjust")
duedate = argv_find(argv, r"\d{8}")
if not duedate:
    duedate = argv_find(argv, r"\d{12}")
print_nosub = not argv_find(argv, "--timeonly")
print_late = not argv_find(argv, "--nosub")
if argv_find(argv, "--summary"):
    print_nosub = False
    print_late = False
    
dst = None
if argv_find(argv, "--dst"):
    dst = True
elif argv_find(argv, "--nodst"):
    dst = False

output(adjust, duedate, print_nosub, print_late, dst)

