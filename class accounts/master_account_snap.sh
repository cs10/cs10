#! /bin/bash

# CS10 Login Script
# By Michael Ball September 9, 2013
# This script was added in Fa13 to make master accounts easier for Snap!
# CURRENTLY THIS IS ONLY EFFECTIVE FOR OS X
# There are 3 things which this script does: (or should do!)
# Set Chrome as default browser
# Add Chrome to OS X dock
# Symlink the BYOB media folder to the user's desktop
# 
# NOTES:
# =============================================== 
# This should only run on initial login (TODO)
# There should be an option for Ubuntu (no BYOB there) (TODO)
# I want to enable screen zoom by default... #TODO
# add the Media link to the dock as well
# Oh and this needs testing.

# Check for OS Version
os=`uname`

if [ $os -eq "Darwin" ]; then
    # Set Chrome to be the default browser
    # TODO for future
    # 
    
    # Check Dock for Chrome
    chrome=`defaults read com.apple.dock persistent-apps | grep "Google Chrome"`
    if [ "$chrome" -eq "" ]; then
        # grep returned no chrome so add it
        defaults write com.apple.dock persistent-apps -array-add "<dict><key>tile-data</key><dict><key>file-data</key><dict><key>_CFURLString</key><string>/Google Chrome.app</string><key>_CFURLStringType</key><integer>0</integer></dict></dict></dict>"
        killall Dock # Dock must be restarted
    fi
    
    link="~/Desktop/SnapMedia"
    if [ ! -L "$link" ]; then
        # if no link exists, add one
        ln -s "/Applications/BYOB 3.1 Mac/Media" ~/Desktop/SnapMedia
    fi
fi

exit 0
    

