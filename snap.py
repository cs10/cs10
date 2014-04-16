"""
BJC Besides Blocks
This sets up mappings to make Snap! behave a bit more like Python
It is designed to be compatible with both 2.6+ and 3.3+ for use with online
interpreters where possible.
Functions should be heavily commented and readable by a novice.

Most all Snap! blocks need to be written as a custom function, however!
When it's not necessary, they're going to be translated directly in the CS10
Besides Blocks project, here:
http://snap.berkeley.edu/snapsource/snap.html#present:Username=cycomachead&ProjectName=cs10bb
TODO: Move this project to cs10 snap account...

The basic header sets inputs and variables that are global to the entire script.
Individual functions import modules as necessary.

Currently, this is designed to be done 1 script at a time, with only one sprite.
TODO:
* Consider adding support for naming Python variables based on Snap! project
parameters -- this could mean LOTS of 'joins' in Snap!.
* Handle multiple sprite interactions
* Broadcasts?
* Media files -- this isn't currently possible.
* Tools, and other libraries support
"""
# Basic Environment Setup
# __future__ must be first in a python program! Needed for 2.6+ only.
from __future__ import division, print_function
# For sprites, pens, and the timer
import turtle, time
# Setup a Global time.
__TIME = time.time()
# Global answer variable
__ANSWER = ''
# Set a turbo mode checker
__TURBO_ON = False
# Create a 'Sprite'
__SPRITE = turtle.Turtle()
turtle.mode('logo')
__SPRITE.up()
__SPRTIE.speed(10)
# Doesn't account for bigger snap stages.
turtle.screensize(320, 480)


def notImplemented(b):
    print(b + " has not been implemented.\n")

###############################################################################
# MOTION BLOCKS #
###############################################################################
"""
The command blocks with dropdowns need functions:
point-towards() -- at least we can probably do mouse-pointer
go-to() -- [same as above]
glide for -- not sure?
if edge, bounce -- probably needs some more code?

All others can directly map to python by referencing __SPRITE
SNAP MAPPINGS:
move 10 steps: __SPRITE.forward(steps)
turn right 15: __SPRITE.right(angle)
...
"""
###############################################################################
# CONTROL BLOCKS #
###############################################################################
"""
No idea if we can map hat blocks... it'd be totally possible to map key commands
Most of these could be very simply mapped w/in snap.

wait-until may be tricky... Or we could just make a blocking while loop?
Not much belongs in this section, honestly.
"""

###############################################################################
# LOOKS BLOCKS #
###############################################################################
"""
Many of these features won't work... (Costumes, gfx effects)

"""

def snapSay(msg, sec):
    return None

def snapSay(msg):
    """
    Does this need to 'clear' before saying?? MUST INVESTIGATE...
    """


###############################################################################
# SENSING BLOCKS #
###############################################################################
def snapKeyDown(key):
    """
    Is this going to be hard to write? If it's a 1 or two liner, it shouldnt be
    here...
    """

"""
Where we can we should implement sensing functions...

MOUSEDOWN? Should hopefully be easy to emulate...
"""
def snapTouchingColor(clr):
    # This should be doable
    return False


# Mapping for Turbo mode settings
def snapSetTurbo(value):
    """
    Change the settings for turbo mode
    """
    # If value isn't a boolean, exit.
    if not isinstance(value, bool):
        return
    
    _TURBO_ON = value
    if _TURBO_ON:
        _SPRITE.speed(0) # disable all sprite animations, go fast as possible.
    else:
        _SPRITE.speed(9)
        

# Mapping for Snap! http:// block
def snapGetURL(url):
    # Import the proper URL library for python 2 or 3
    try:
        from urllib2 import urlopen
    except:
        from urllib.request import urlopen

    u = urlopen('http://' + str(url))
    raw = u.readall()
    # encodingA = u.getheader('Accept-Charset')
    # encodingB = u.getheader('Context-Type')
    # Currently try decoding as UTF-8, but we could be smarter
    try:
        return raw.decode('utf-8')
    except: # Can't decode, just return raw data.
        return raw

# Mapping for Snap! current(DATE) block
def snapCurrentDate(item):
    """
    item should be one of:
    year, month, date, day of week, hour, minute, second, time in milliseconds
    Note, in practice, you could make this code more compact with more complex
    syntax, but we're hoping to make things easily readable and understandable.
    """
    from datetime import datetime
    now = datetime.now()
    if item == 'year':
        return now.year
    elif item == 'month':
        return now.month
    elif item == 'date':
        return now.date
    elif item == 'day of week':
        # Snap weekdays are 1-7 sunday-saturday, Python is 0-6 monday to Sunday
        day = (now.weekday() + 2) % 7
        # Make sat be 7 instead of 0, since we used mod.
        return day if day != 0 else 7
    elif item == 'hour':
        return now.hour
    elif item == 'minute':
        return now.minute
    elif item == 'second':
        return now.second
    elif item == 'time in milliseconds':
        return time.time() #time module must be imported! (We did this already)
    else:
        return ''
        
# Map ask X and wait in Snap
def ask(quest):
    """
    Return an answer from the terminal, but this is Python 2.x and 3.x safe.
    """
    try:
        ans = raw_input(quest + ' ') # Python 2
    except NameError:
        ans = input(quest + ' ') # Python 3
    
    return ans
###############################################################################
# SOUNDS BLOCKS #
###############################################################################
"""
These are gonna be hard to do, so skip this section for now.
"""

###############################################################################
# OPERATORS BLOCKS #
###############################################################################
"""
There's potentially a lot of tricky stuff in here...
TODO: See if we can simply map rings to Lambdas? idk about input params though?
"""

# Mapping for Snap! split block
def snapSplit(st, delim):
    """
    Split items, if not delimeter is provided, split by strings.
    """
    st = str(st) # force conversion to string, if input isn't already.
    if delim == '':
        return list(st)
    return st.split(delim)

# Mapping for Random Numbers
def snpGetRandom(start, stop):
    """
    You must import the random module in Python for random numbers.
    The randint function is inclusive, just like Snap!'s
    """
    from random import randint
    return randint(start, stop) 


# Mapping for Snap! math function block
def snapMath(fn, num):
    """
    """
    return None # FIXME

###############################################################################
# PEN BLOCKS #
###############################################################################
"""
Most of this SHOULD be straightforward
NEED to test pen size
"""
def snapSetColor(clr):
    """
    Scratch has a crazy color number format. :(
    """


###############################################################################
# VARIABLES BLOCKS #
###############################################################################
"""
Lists functions work ok because pointers. Yay pointers.
"""

# Mapping for the item of block for lists
def snapItemOf(n, lst):
    """
    This is a pretty simple function, but handles the 'any' and 'last' options.
    In Python, it's generally bad to name variables the same as built in
    functions, so we use 'lst' instead of 'list'.
    """
    if len(lst) < 1:
        return ''
    if n == 'any':
        from random import choice
        return choice(lst)
    elif n == 'last':
        return lst[len(lst) - 1]
    else:
        return lst[n - 1]

# Mapping for Snap! Delete Iten
def snapDelete(n, lst):
    """
    This is a pretty simple function, but handles the 'all' and 'last' options.
    In Python, it's generally bad to name variables the same as built in
    functions, so we use 'lst' instead of 'list'.
    """
    if n == 'all':
        del lst[:] # lst[:] selects all items in the list.
    elif n == 'last':
        lst.pop(len(lst) - 1) # pop removes the given item from a list.
    else:
        lst.pop(n - 1)

# Mapping for Snap! Insert At block
def snapInsertAt(n, lst, item):
    """
    This is a pretty simple function, but handles the 'any' and 'last' options.
    In Python, it's generally bad to name variables the same as built in
    functions, so we use 'lst' instead of 'list'.
    """
    if n == 'any':
        from random import randrange
        pos = randrange(0, len(lst) + 1) # randrange is NOT inclusive.
        lst.insert(pos, item)
    elif n == 'last':
        return lst[lst.length - 1]
    else:
        return lst[n - 1]

# Mapping for Snap! Replace Item bloc
def snapReplaceItem(n, lst, item):
    """
    This is a pretty simple function, but handles the 'any' and 'last' options.
    In Python, it's generally bad to name variables the same as built in
    functions, so we use 'lst' instead of 'list'.    
    """
    if n == 'any':
        from random import randrange
        pos = randrange(0, len(lst))
        lst[pos] = item
    elif n == 'last':
        lst[len(lst) - 1] = item
    else:
        lst[n - 1] = item
