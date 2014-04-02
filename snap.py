"""
BJC Beyond Blocks
This sets up mappings to make Snap! behave a bit more like Python
It is designed to be compatible with both 2.6+ and 3.3+ for use with online
interpreters where possible.
Functions should be heavily commented and readable by a novice.

Most all Snap! blocks need to be written as a custom function, however!
When it's not necessary, they're going to be translated directly in the CS10
Beyond Blocks project, here:
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
__TURBO = False
# Create a 'Sprite'
__SPRITE = turtle.Turtle()

# FIXME
# Set Window Dimensions
# Directions to be like logo
# Set the pen to be up
# Set the speed and animation


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
    
def snapKeyDown(key):
    """
    Is this going to be hard to write? If it's a 1 or two liner, it shouldnt be
    here...
    """
    

###############################################################################
# SENSING BLOCKS #
###############################################################################
"""
Where we can we should implement sensing functions...

MOUSEDOWN? Should hopefully be easy to emulate...
"""
def snapTouchingColor(clr):
    # This should be doable
    return False
    
# Mapping for Snap! http:// block
def getURL(url):
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
def current(item):
    """
    item should be one of:
    year, month, date, day of week, hour, minute, second, time in milliseconds
    """
    return None # FIXME

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
    """
    if delim == '':
        return list(st)
    return st.split(delim)
    
# Mapping for Random Numbers
def getRandom(start, stop):
    """
    FIXME!
    """
    return 4
    
    
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
Lists pose a real issue with the way code mapping is currently setup...
We could try doing something with nonlocal / global, or we can subclass and
override the built in list object:
http://stackoverflow.com/questions/4698493/can-i-add-custom-methods-attributes-to-built-in-python-types

If we do that, then the basic header for MAIN would need to include the list stuff
"""
    
# Mapping for the item of block for lists
def snapItemOf(n, lst):
    """
    This is a pretty simple function, but handles the 'any' and 'last' options.
    """
    if n == 'any':
        # import random
        return 0 # FIXME
    elif n == 'last':
        return lst[lst.length - 1]
    else:
        return lst[n - 1]
        
# Mapping for Snap! Delete Iten
def snapDelete(n, lst):
    """
    This is a pretty simple function, but handles the 'any' and 'last' options.
    """
    # FIXME -- this isn't very easily functionalized!
    if n == 'any':
        # import random
        return 0 # FIXME
    elif n == 'last':
        return lst[lst.length - 1]
    else:
        return lst[n - 1]
        
# Mapping for Snap! Insert At block
def snapInsertAt(n, lst):
    """
    This is a pretty simple function, but handles the 'any' and 'last' options.
    """
    # FIXME -- this isn't very easily functionalized!
    if n == 'any':
        # import random
        return 0 # FIXME
    elif n == 'last':
        return lst[lst.length - 1]
    else:
        return lst[n - 1]
        
# Mapping for Snap! Replace Item bloc
def snapReplaceItem(n, lst, new):
    """
    This is a pretty simple function, but handles the 'any' and 'last' options.
    """
    # FIXME -- this isn't very easily functionalized!
    if n == 'any':
        # import random
        return 0 # FIXME
    elif n == 'last':
        return lst[lst.length - 1]
    else:
        return lst[n - 1]
