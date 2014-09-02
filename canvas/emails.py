#! /usr/bin/env python3

michael_path = '/Volumes/Macintosh HD/Users/Michael/Dropbox/Projects/'
import sys
sys.path.append(michael_path + 'canvaslms/canvaslms')

import canvaslms.api as api

# Get the authorization token from a file (Or from any other source.
#   We just need a string containing the authorization token.
authToken = api.getAuthTokenFromFile(michael_path + 'canvas_token.txt')
# Create our API object, giving the name of the server running the
#   instance of Canvas and the authorization token that we'll use to
#   authenticate our requests.
apiObj = api.CanvasAPI('https://bcourses.berkeley.edu', authToken)

stuemails = []
staffemails = []

base = 'https://bcourses.berkeley.edu/api/v1/'
cs10base = base + 'courses/1246916/'
url = cs10base + 'users?&include[]=email&per_page=550&enrollment_type='

cs10stu = apiObj.allPages(url + 'student', absoluteUrl=True, verbose=True)
cs10staff = apiObj.allPages(url + 'ta', absoluteUrl=True, verbose=True)

for stu in cs10stu:
    usremail = stu['email']
    stuemails.append(usremail)

for staff in cs10staff:
    usremail = staff['email']
    staffemails.append(usremail)

print(stuemails)
print()
print(staffemails)
