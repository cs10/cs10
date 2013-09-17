import datetime
import os
import sys
import traceback
#import urllib

gVerbose = True
gGenerateWeekly = True
gGenerateSemester = False
gOpenResults = True
gSquelchQuotes = True
gCommasAddNewline = False
gAddIDAndTitleCalendarHack = True
gReplaceCaretWithBullet = True

gWeeklyFileName = "weekly"
gSemesterFileName = "semester"

gInputExtension = ".txt"
gOutputExtension = ".html"

# Weekly column header search strings
gTimeColumnContains = "time"
gDaysColumnStartsAt = "monday"
gSectionColumnContains = "section"
gTAColumnContains = "ta"
gOfficeHoursColumnContains = "office"

# Semester column header search strings
gDueWhatColumnContains = "due"
gDueWeekColumnContains = "week"
gDueDayColumnContains = "day"
gDueTimeColumnContains = "time"
gLecturesColumnContains = "lecture"
gDueDatesColumnContains = "due"
gReadingsColumnContains = "read"

# Common column header search strings
gLinkNumberColumnContains = "number"
gLinkColumnContains = "link"
gLabsColumnContains = "lab"
gDiscussionsColumnContains = "disc"

gPrefixHTML = """
<!DOCTYPE html>
<html>
<head>
    <link href="../scripts/cs10style.css" title="CS10 Style" rel="stylesheet" type="text/css" />
    <title>UC Berkeley EECS | CS10 : The Beauty and Joy of Computing | #SEMESTER #YEAR</title>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />    
    <meta name="generator" content="Scheduler by Glenn Sugden" />
</head>
<body>
<!--                                         START CUT HERE                                         -->

"""

gSuffixHTML = """
<!--                                         END CUT HERE                                         -->
</body>
</html>
"""

gWeeklyTableHeaders = ( "Hour", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday" )
gWeeklyTableRowPrefixHTML = """\t\t<tr class="weekCalendarRow">\r"""
gWeeklyTableCellCalendarCSSClassHTML = "calendar"

gSemesterTableHeaders = ( "Week", "Days in #YEAR", "Readings (Sa/Su)", "Lecture 1 (#LECTURE1DAY)", "Lab 1 (#LAB1DAY1/#LAB2DAY1)", "Lecture 2 (#LECTURE2DAY)", "Lab 2 (#LAB1DAY2/#LAB2DAY2)", "Discussion (#DISCUSSIONDAY)", "HW & Projects Due" )
gSemesterTableRowPrefixHTML = """\t\t<tr class="calendar#ALTERNATECSSROW">\r"""
gSemesterTableCellCalendarCSSClassHTML = "calendar#ALTERNATECSSCOLUMN"

gTablePrefixHTML = """\t<table width="100%">\r"""
gTableRowSuffixHTML = """\t\t</tr>\r"""
gTableCellPrefixHTML = """\t\t\t<#CELLTYPE align="#ALIGN"#ID#TITLE class="#CLASS" width="#PERCENT%"#ROWSPAN#COLSPAN>"""
gTableSuffixHTML = """\t</table>\r"""

gTableCellLabCSSClassHTML = "lab"
gTableCellDiscussionCSSClassHTML = "disc"
gTableCellOfficeHoursCSSClassHTML = "oh"
gTableCellLectureCSSClassHTML = "lecture"
gSemesterTableCellNoCSSClassHTML = "noClass"

gDayNames = ( "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" )

def warning( warningString ):
    line = traceback.extract_stack()[-2][1]
    func = traceback.extract_stack()[-2][2]
    if ( func == "<module>" ):
        func = "<main>"
    sys.stdout.write( "--- WARNING --- in " + func + " at line #" + str( line ) + ": " + warningString + "\r" )

def error( errorString ):
    sys.stderr.write( "*** ERROR *** " + errorString + "\r" )
    traceback.print_stack()
    sys.exit( 2 )

def openFile( filename, writing = False ):
    fref = None
    try:
        if ( writing == False ):
            fref = open( filename, "rU" )
        else:
            fref = open( filename, "w" )
    except:
        errorString = "Unable to open " + filename + " for "
        if ( writing == False ):
            errorString = errorString + "input"
        else:
            errorString = errorString + "output"
        errorString = errorString + "."
        error( errorString )
    return fref

def readNextColumns( fref ):
    columns = None
    try:
        columns = fref.readline().split( "\t" )
        for colIndex in range( 0, len( columns ) ):
            columns[colIndex] = columns[colIndex].rstrip().lstrip()
    except:
        error( "Couldn't read columns from input file." )
    return columns

def findColumnInHeaders( headers, columnName ):
    """ Look for the a column in a list of headers that contains the text columnName """
    column = -1
    index = 0
    for header in headers:
        if columnName in header.lower():
            column = index
            break
        else:
            index = index + 1
    if column == -1:
        error( """Couldn't find a header with the word '""" + columnName + """' in it !
        Headers: """ + str( headers ) )
    else:
        if gVerbose:
            print "'" + columnName + "'", "header column found at:", column
    return column

def processLinkList( fref ):
    originalFilePosition = fref.tell() # Links have been moved to the end of the file, so save the current position so we can rewind it
    linkList = [""]
    # Find column headers we need
    foundIt = False
    while( foundIt == False ): # FIXME: Potential for infinite loop
        headers = readNextColumns( fin )
        if ( headers == None ):
            error( "ABORTING" )
        for header in headers:
            if gLinkColumnContains in header.lower():
                foundIt = True
    linkNumberColumn = findColumnInHeaders( headers, gLinkNumberColumnContains )
    linkColumn = findColumnInHeaders( headers, gLinkColumnContains )
    while( True ):
        columns = readNextColumns( fref )
        if ( len( columns[0] ) > 0 ):
            # Extend the list until it has enough space to hold this link
            linkNumber = int( columns[linkNumberColumn] )
            while( ( len( linkList ) - 1 ) < linkNumber ):
                linkList.append( "" )
            theLink = columns[linkColumn]
            theURL = theLink[theLink.find( "//" ) + 2:]
            linkList[linkNumber] = theLink[:theLink.find( "//" ) + 2] + theURL.replace( "&", "&amp;" ) #urllib.quote( theURL ) creates bad SAGE URLs?
        else:
            break
    if ( gVerbose ):
        print "LinkList:", linkList
    fref.seek( originalFilePosition )
    return linkList

def getDayFromIndex( dayIndex ):
    if ( dayIndex == None ):
        return "(None)"
    else:
        return gDayNames[dayIndex]

def getShortDayFromIndex( dayIndex ):
    if ( dayIndex == None ):
        return "(None)"
    elif ( ( gDayNames[dayIndex][0] == 'T' ) or ( gDayNames[dayIndex][0] == 'S' ) ):
        return gDayNames[dayIndex][:2]
    else:
        return gDayNames[dayIndex][0]

def getDateOffsetFromDayOfWeek( startDate, dayOfTheWeek ):
    daysOfTheWeek = ( "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" )
    if ( dayOfTheWeek in daysOfTheWeek ):
        dayOffset = daysOfTheWeek.index( dayOfTheWeek )
        return ( startDate + datetime.timedelta( days = dayOffset ) )
    else:
        error( '''Couldn't find the day of the week "''' + dayOfTheWeek + '" in ' + str( daysOfTheWeek ) )

def makeDateFromString( dateString ):
    if ( '.' in dateString ):
        dateFields = dateString.split( "." )
    elif ( '-' in dateString ):
        dateFields = dateString.split( "-" )
    else:
        error( "Couldn't figure out the starting date delimiter: " + dateString )
    return( datetime.date( int( dateFields[0] ), int( dateFields[1] ), int( dateFields[2] ) ) )

def replaceLinks( inString, linkList ):
    resultString = inString
    if ( len( resultString ) >= 3 ): #Must have at last a length of 3 to have "#1 "
        while ( True ):
            for cIndex in range( 0, len( resultString ) ):
                if resultString[cIndex] == '{':
                    endFontString = ''
                    linkNumString = ""
                    lIndex = cIndex + 1
                    while( ( lIndex < len( resultString ) ) and ( resultString[lIndex] != '}' ) ):
                        linkNumString = linkNumString + resultString[lIndex]
                        lIndex = lIndex + 1
                    try:
                        linkNumber = int( linkNumString )
                    except ValueError as exception:
                        print "Error converting " + linkNumString + " to a number in " + inString + ":"
                        print exception
                    if ( linkNumber < len( linkList ) ):
                        if ( linkList[linkNumber][0] == '*' ):
                            if ( linkList[linkNumber][1] == '*' ):
                                resultString = resultString.replace( "{" + str( linkNumber ) + "}" , '''<a href="''' + linkList[linkNumber][2:] + '''"><font color="#008000"><i>''' )
                                endFontString = '</i></font>'
                            else:
                                resultString = resultString.replace( "{" + str( linkNumber ) + "}" , '''<a href="''' + linkList[linkNumber][1:] + '''"><font color="#800000">''' )
                                endFontString = '</font>'
                        else:
                            resultString = resultString.replace( "{" + str( linkNumber ) + "}" , '''<a href="''' + linkList[linkNumber] + '''">''' )
                        resultString = resultString.replace( "{" + str( linkNumber ) + "}" , '''<a href="''' + linkList[linkNumber] + '''">''' )
                    else:
                        error( "Link reference too high: " + str( linkNumber ) + " when the maximum is: " + str( len( linkList ) - 1 ) )
                    for eIndex in range( cIndex, len( resultString ) ):
                        if resultString[eIndex] == '}':
                            resultString = resultString[:eIndex] + endFontString + "</a>" + resultString[eIndex + 1:]
                            break
                    break
            if ( cIndex == len( resultString ) - 1 ):
                break
    return resultString.lstrip().rstrip()

def writeCell( fout, label, cellClass, percentWidth, linkList, align = "center", cellID = None, title = None, rowSpan = 1, columnSpan = 1, isHeader = False, highlightBorder = False ):
    if ( type( linkList ) != type( [] ) ):
        raise Exception( "writeCell passed a number instead of a linkList!" )
    rowSpanString = ""
    columnSpanString = ""
    cellTypeString = "td"
    idString = ""
    titleString = ""
    if ( cellID != None ):
        idString = ' id="' + str( cellID ) + '"'
    if ( title != None ):
        titleString = ' title="' + title + '"'
    if ( rowSpan > 1 ):
        rowSpanString = ' rowspan="' + str( rowSpan ) + '"'
    if ( columnSpan > 1 ):
        columnSpanString = ' colspan="' + str( columnSpan ) + '"'
    if ( isHeader == True ):
        cellTypeString = "th"
    cellPrefixString = gTableCellPrefixHTML
    cellPrefixString = cellPrefixString.replace( "#CELLTYPE", cellTypeString )
    if ( highlightBorder ):
        cellPrefixString = cellPrefixString.replace( "#CLASS", cellClass + '''" style="border:solid 1px #C88''' )
    else:
        cellPrefixString = cellPrefixString.replace( "#CLASS", cellClass )
    cellPrefixString = cellPrefixString.replace( "#ID", idString )
    cellPrefixString = cellPrefixString.replace( "#TITLE", titleString )
    cellPrefixString = cellPrefixString.replace( "#PERCENT", str( percentWidth ) )
    cellPrefixString = cellPrefixString.replace( "#ROWSPAN", rowSpanString )
    cellPrefixString = cellPrefixString.replace( "#COLSPAN", columnSpanString )
    cellPrefixString = cellPrefixString.replace( "#ALIGN", align )
    fout.write( cellPrefixString )
    # FIXME: Hacky
    label = label.replace( "&#", "`" )
    label = label.replace( "&", "&amp;" )
    label = label.replace( "`", "&#" )
    if ( gSquelchQuotes ):
        label = label.replace( '''"''', "" )
    if ( gCommasAddNewline ):
        label = label.replace( ',', ",<br />" )
    if ( gReplaceCaretWithBullet ):
        if ( "^" in label ):
            label = label.replace( "^", "&bull; " )
            label = label.replace( ', ', "<br />" )
    labelWithLinks = replaceLinks( label, linkList )
    fout.write( labelWithLinks )
    fout.write( "</" + cellTypeString + ">\r" )

# MAIN

if ( gVerbose ):
    print "Verbose output = TRUE"

# WEEKLY SCHEDULE

if ( gGenerateWeekly ):

    fin = openFile( gWeeklyFileName + gInputExtension, False )

    # Store links

    linkList = processLinkList( fin )

    # Lecture location

    lectureLocRow = readNextColumns( fin )
    if ( lectureLocRow == None ):
        error( "ABORTING" )

    lectureLocation = lectureLocRow[1]

    if ( gVerbose ):
        print "Lecture location:", lectureLocation

    blankLine = readNextColumns( fin ) # Skip blank line
    if ( blankLine == None ):
        error( "ABORTING" )

    # Find column section headers we need

    sectionHeaders = readNextColumns( fin )
    if ( sectionHeaders == None ):
        error( "ABORTING" )

    sectionColumn = findColumnInHeaders( sectionHeaders, gSectionColumnContains )
    nameColumn = findColumnInHeaders( sectionHeaders, gTAColumnContains )
    labColumn = findColumnInHeaders( sectionHeaders, gLabsColumnContains )
    discussionColumn = findColumnInHeaders( sectionHeaders, gDiscussionsColumnContains )
    officeColumn = findColumnInHeaders( sectionHeaders, gOfficeHoursColumnContains )

    # Gather TA Data (section #, etc.)
    sectionData = {}
    while( True ):
        columns = readNextColumns( fin )
        if ( len( columns[0] ) > 0 ):
            sectionData[columns[sectionColumn]] = { sectionHeaders[nameColumn]:columns[nameColumn], sectionHeaders[labColumn]:columns[labColumn], sectionHeaders[discussionColumn]:columns[discussionColumn], sectionHeaders[officeColumn]:columns[officeColumn] }
        else:
            break

    # Find column headers we need

    headers = readNextColumns( fin )
    if ( headers == None ):
        error( "ABORTING" )

    timeColumn = findColumnInHeaders( headers, gTimeColumnContains )
    daysStart = findColumnInHeaders( headers, gDaysColumnStartsAt )

    fout = openFile( gWeeklyFileName + gOutputExtension, True )
    fout.write( gPrefixHTML )
    fout.write( gTablePrefixHTML )

    fout.write( gWeeklyTableRowPrefixHTML )

    width = 7 # Percent, for the first column
    for tableHeader in gWeeklyTableHeaders:
        writeCell( fout, tableHeader, gWeeklyTableCellCalendarCSSClassHTML, width, linkList, rowSpan = 1, isHeader = True )
        width = 14 # Percent, for the remaining columns

    fout.write( gTableRowSuffixHTML )

    lecture1Day = None
    lecture2Day = None
    lab1Day1 = None
    lab1Day2 = None
    whichLab1Day = None # Which lab is considered as one of the (pair of) days that set the semester lab days?
    lab2Day1 = None
    lab2Day2 = None
    whichLab2Day = None  # Which other lab is considered as one of the (pair of) days that set the semester lab days?
    discussionDay = None

    # Set up a "read-ahead" buffer (one line), so we can rowspan (e.g. "Labs")

    prevColumns = None
    nextColumns = readNextColumns( fin )

    while( True ):
        prevColumns = columns
        columns = nextColumns
        nextColumns = readNextColumns( fin )
        if ( len( columns[0] ) > 0 ):
            fout.write( gWeeklyTableRowPrefixHTML )
            width = 7 # Percent, for the first column
            hour = int( columns[timeColumn] )
            if ( hour == 12 ):
                timeString = "12:00"
            else:
                timeString = str( hour % 12 ) + ":00"
            if ( hour >= 12 ):
                timeString = timeString + "pm"
            else:
                timeString = timeString + "am"
            writeCell( fout, timeString, gWeeklyTableCellCalendarCSSClassHTML, width, linkList )
            for dayIndex in range( 0, 5 ):
                thisRowSpan = 1
                labelString = columns[daysStart + dayIndex]
                whichPrefixString = ""
                whichString = ""
                whoString = ""
                whereString = "<br />"
                if ( ( len( labelString ) > 1 ) and ( "lecture" not in labelString.lower() ) ):
                        whichString = labelString[-1] # HACKish way to strip the trailing number off for the section digit - SINGLE DIGITS ONLY
                        labelString = labelString[:-2]
                        whoString = "<br />(" + sectionData[whichString][sectionHeaders[nameColumn]] + ")"
                if ( len( columns[daysStart + dayIndex] ) == 0 ):
                    classString = gWeeklyTableCellCalendarCSSClassHTML
                elif ( "lecture" in columns[daysStart + dayIndex].lower() ): # Lecture
                    whereString = whereString + lectureLocation
                    classString = gTableCellLectureCSSClassHTML
                    # Store lecture days for semester calendar
                    if ( lecture1Day == None ):
                        lecture1Day = dayIndex
                        if ( gVerbose ):
                            print "lecture1Day=" + getDayFromIndex( dayIndex ) + " (" + str( dayIndex ) + ")"
                    elif ( lecture2Day == None ):
                        lecture2Day = dayIndex
                        if ( gVerbose ):
                            print "lecture2Day=" + getDayFromIndex( dayIndex ) + " (" + str( dayIndex ) + ")"
                    elif ( ( lecture1Day != dayIndex ) and ( lecture2Day != dayIndex ) ):
                        warning( "More than two lecture days? " + getDayFromIndex( lecture1Day ) + " or " + getDayFromIndex( lecture2Day ) + " != " + getDayFromIndex( dayIndex ) )
                        warning( "Current columns: " + str( columns[daysStart:daysStart + 5] ) )
                elif ( "lab" in columns[daysStart + dayIndex].lower() ): # Lab
                    whichPrefixString = "01"
                    whereString = whereString + sectionData[whichString][sectionHeaders[labColumn]]
                    classString = gTableCellLabCSSClassHTML
                    # Store lab days for semester calendar
                    if ( lab1Day1 == None ):
                        whichLab1Day = whichString
                        lab1Day1 = dayIndex
                        if ( gVerbose ):
                            print "lab1Day1=" + getDayFromIndex( dayIndex ) + " (" + str( dayIndex ) + ")"
                    elif ( ( lab1Day2 == None ) and ( whichLab1Day == whichString ) ):
                        lab1Day2 = dayIndex
                        if ( gVerbose ):
                            print "lab1Day2=" + getDayFromIndex( dayIndex ) + " (" + str( dayIndex ) + ")"
                    elif ( ( lab2Day1 == None ) and ( lab1Day1 != dayIndex ) and ( lab1Day2 != dayIndex ) ):
                        whichLab2Day = whichString
                        lab2Day1 = dayIndex
                        if ( gVerbose ):
                            print "lab2Day1=" + getDayFromIndex( dayIndex ) + " (" + str( dayIndex ) + ")"
                    elif ( ( lab2Day2 == None ) and ( whichLab2Day == whichString ) ):
                        lab2Day2 = dayIndex
                        if ( gVerbose ):
                            print "lab2Day2=" + getDayFromIndex( dayIndex ) + " (" + str( dayIndex ) + ")"
                        # Swap the pairs if the days are out of (chronological) order
                        if ( lab1Day1 > lab2Day1 ):
                            if ( gVerbose ):
                                print "Swapping out of (chronological) order lab day pairs."
                            temp = lab1Day1
                            lab1Day1 = lab2Day1
                            lab2Day1 = temp
                            temp = lab1Day2
                            lab1Day2 = lab2Day2
                            lab2Day2 = temp
                    elif ( ( lab1Day1 != dayIndex ) and ( lab1Day2 != dayIndex ) and ( lab2Day1 != dayIndex ) and ( lab2Day2 != dayIndex ) ):
                        warning( "More than four lab days? " + getDayFromIndex( lab1Day1 ) + ", " + getDayFromIndex( lab1Day2 ) + ", " + getDayFromIndex( lab2Day1 ) + ", or " + getDayFromIndex( lab2Day2 ) + " != " + getDayFromIndex( dayIndex ) )
                        warning( "Current columns: " + str( columns[daysStart:daysStart + 5] ) )
                elif ( "discussion" in columns[daysStart + dayIndex].lower() ): # Discussion
                    whichPrefixString = "10"
                    whereString = whereString + sectionData[whichString][sectionHeaders[discussionColumn]]
                    classString = gTableCellDiscussionCSSClassHTML
                    # Store discussion day for semester calendar
                    if ( discussionDay == None ):
                        discussionDay = dayIndex
                        if ( gVerbose ):
                            print "discussionDay=" + getDayFromIndex( dayIndex ) + " (" + str( dayIndex ) + ")"
                    elif ( discussionDay != dayIndex ):
                        warning( "More than one discussion day? " + getDayFromIndex( discussionDay ) + " != " + getDayFromIndex( dayIndex ) )
                        warning( "Current columns: " + str( columns[daysStart:daysStart + 5] ) )
                elif ( "office" in columns[daysStart + dayIndex].lower() ): # Office Hours
                    whereString = whereString + sectionData[whichString][sectionHeaders[officeColumn]]
                    whichString = ""
                    labelString = "Office Hours"
                    classString = gTableCellOfficeHoursCSSClassHTML
                if ( ( len( nextColumns ) > 1 ) and ( nextColumns[daysStart + dayIndex] == columns[daysStart + dayIndex] ) and len( columns[daysStart + dayIndex] ) > 0 ): # RowSpan double hour-ed times (e.g. "Labs")
                    thisRowSpan = 2
                if ( ( ( prevColumns != None ) and ( prevColumns[daysStart + dayIndex] != columns[daysStart + dayIndex] ) ) or ( len( columns[daysStart + dayIndex] ) == 0 ) ): # Don't write a previously double row-spanned cell
                    writeCell( fout, labelString + " " + whichPrefixString + whichString + whoString + whereString , classString, width, linkList, rowSpan = thisRowSpan )
                width = 14 # Percent, for the remaining columns
            fout.write( gTableRowSuffixHTML )
        else:
            break

    fout.write( gTableSuffixHTML )
    fout.write( gSuffixHTML )
    fout.close()

    fin.close()

    # Sanity check (Weekly)

    if ( lecture1Day != None ):
        if ( lecture2Day != None ):
            pass # This is OK
        else:
            warning ( "The second lecture day wasn't found." )
    else:
        warning ( "The first lecture day wasn't found." )

    print "Done with weekly calendar now generating semester calendar..."

else:

    warning( "Skipping weekly calendar generation, not #REPLACEMENTS will _not_ be replaced!..." )

if ( gGenerateSemester ):

    # SEMESTER SCHEDULE

    fin = openFile( gSemesterFileName + gInputExtension, False )

    # Start date

    dateRow = readNextColumns( fin )
    if ( dateRow == None ):
        error( "ABORTING" )

    startingDate = makeDateFromString( dateRow[1] )

    if ( gVerbose ):
        print "Semester starting date:", startingDate

    # Finals date

    dateRow = readNextColumns( fin )
    if ( dateRow == None ):
        error( "ABORTING" )

    finalDate = makeDateFromString( dateRow[1] )

    if ( gVerbose ):
        print "Semester final date:", finalDate

    # Finals date

    dateRow = readNextColumns( fin )
    if ( dateRow == None ):
        error( "ABORTING" )

    endingDate = makeDateFromString( dateRow[1] )

    if ( gVerbose ):
        print "Semester ending date:", endingDate

    blankLine = readNextColumns( fin ) # Skip blank line
    if ( blankLine == None ):
        error( "ABORTING" )

    # Store links

    linkList = processLinkList( fin )

    # Write out the generated HTML file

    fout = openFile( gSemesterFileName + gOutputExtension, True )
    fout.write( gPrefixHTML )
    fout.write( gTablePrefixHTML )

    fout.write( gSemesterTableRowPrefixHTML )

    width = 4 # Percent, for the first column
    for tableHeader in gSemesterTableHeaders:
        tableHeader = tableHeader.replace( "#YEAR", str( startingDate.year ) )
        tableHeader = tableHeader.replace( "#LECTURE1DAY", getShortDayFromIndex( lecture1Day ) )
        tableHeader = tableHeader.replace( "#LECTURE2DAY", getShortDayFromIndex( lecture2Day ) )
        tableHeader = tableHeader.replace( "#LAB1DAY1", getShortDayFromIndex( lab1Day1 ) )
        tableHeader = tableHeader.replace( "#LAB1DAY2", getShortDayFromIndex( lab1Day2 ) )
        tableHeader = tableHeader.replace( "#LAB2DAY1", getShortDayFromIndex( lab2Day1 ) )
        tableHeader = tableHeader.replace( "#LAB2DAY2", getShortDayFromIndex( lab2Day2 ) )
        tableHeader = tableHeader.replace( "#DISCUSSIONDAY", getShortDayFromIndex( discussionDay ) )
        writeCell( fout, tableHeader, gSemesterTableCellCalendarCSSClassHTML.replace( "#ALTERNATECSSCOLUMN", "" ), width, linkList, rowSpan = 1, isHeader = True )
        width = 12 # Percent, for the remaining columns

    fout.write( gTableRowSuffixHTML )

    # Read in holidays

    holidays = []

    while ( True ):
        columns = readNextColumns( fin )
        if ( columns == None ):
            error( "ABORTING" )
        elif ( len( columns[0] ) == 0 ):
            break
        else:
            holidays.append( ( makeDateFromString( columns[1] ), columns[0] ) )

    if ( gVerbose ):
        print "Holidays:", holidays

    headers = readNextColumns( fin )
    if ( headers == None ):
        error( "ABORTING" )

    # Read in what's due

    dueWhat = findColumnInHeaders( headers, gDueWhatColumnContains )
    dueWeek = findColumnInHeaders( headers, gDueWeekColumnContains )
    dueDay = findColumnInHeaders( headers, gDueDayColumnContains )
    dueTime = findColumnInHeaders( headers, gDueTimeColumnContains )

    whatsDues = {}

    while ( True ):
        columns = readNextColumns( fin )
        if ( columns == None ):
            error( "ABORTING" )
        if ( len( columns[0] ) > 0 ):
            weekDate = startingDate + datetime.timedelta( weeks = int( columns[ dueWeek ] ) )
            whatsDues[getDateOffsetFromDayOfWeek( weekDate, columns[dueDay] )] = ( columns[dueWhat], columns[dueDay], columns[dueTime] )
        else:
            break

    if ( gVerbose ):
        print "whatsDues:", whatsDues

    # Read in the rest of the schedule

    headers = readNextColumns( fin )
    if ( headers == None ):
        error( "ABORTING" )

    readingsColumn = findColumnInHeaders( headers, gReadingsColumnContains )
    lecturesColumn = findColumnInHeaders( headers, gLecturesColumnContains )
    labsColumn = findColumnInHeaders( headers, gLabsColumnContains )
    discussionsColumn = findColumnInHeaders( headers, gDiscussionsColumnContains )

    readings = []
    lectures = []
    labs = []
    discussions = []

    while ( True ):
        columns = readNextColumns( fin )
        if ( columns == None ):
            error( "ABORTING" )
        elif ( len( columns[1] ) > 0 ):
            readings.append( columns[readingsColumn] )
            lectures.append( columns[lecturesColumn] )
            labs.append( columns[labsColumn] )
            if ( ( len( columns ) > discussionsColumn ) and ( len( columns[discussionsColumn] ) > 1 ) ):
                discussions.append( columns[discussionsColumn] )
        else:
            break

    if ( gVerbose ):
        print "lectures: ", lectures
        print "labs:", labs
        print "discussions:", discussions
        print "whatsDues:", whatsDues

    whichWeek = 1
    alternateRow = False
    currentDate = startingDate
    whichReading = 0
    whichLecture = 0
    whichLab = 0
    whichDisc = 0
    whichDue = 0
    whichHoliday = 0

    while( currentDate < endingDate ):
        duesThisWeek = []
        if ( whichWeek % 2 ):
            alternateCSSRowString = "2"
        else:
            alternateCSSRowString = ""
        fout.write( gSemesterTableRowPrefixHTML.replace( "#ALTERNATECSSROW", alternateCSSRowString ) )
        # Week
        writeCell( fout, str( whichWeek ), gWeeklyTableCellCalendarCSSClassHTML.replace( "#ALTERNATECSSCOLUMN", alternateCSSRowString ), 4, linkList )
        # Days
        writeCell( fout, currentDate.strftime( "%b %d" ) + " -<br />" + ( currentDate + datetime.timedelta( days = 5 ) ).strftime( "%b %d" ),
                   gSemesterTableCellCalendarCSSClassHTML.replace( "#ALTERNATECSSCOLUMN", alternateCSSRowString ), 12, linkList )
        # Reading
        writeCell( fout, readings[whichWeek - 1], gSemesterTableCellCalendarCSSClassHTML.replace( "#ALTERNATECSSCOLUMN", alternateCSSRowString ), 12, linkList, align = "left" )
        # Days
        while ( currentDate.weekday() <= 4 ):
            labelString = ""
            doHighlight = False
            if ( gAddIDAndTitleCalendarHack ):
                calendarMonthIDHack = currentDate.month
                calendarDayTitleHack = str( currentDate.day )
            else:
                calendarMonthIDHack = None
                calendarDayTitleHack = None
            if ( whatsDues.has_key( currentDate ) ):
#                   labelString = labelString + "<br /><br /><i>Due: " + whatsDues[currentDate][0] + "</i>"
                doHighlight = True
                duesThisWeek.append( whatsDues[currentDate] )
            if ( ( whichHoliday < len( holidays ) ) and ( currentDate == holidays[whichHoliday][0] ) ): # Process holidays
                colspan = 1 # FIXME
                cssClass = gSemesterTableCellNoCSSClassHTML
                labelString = labelString + holidays[whichHoliday][1]
                whichHoliday = whichHoliday + 1
            else:
                colspan = 1
                cssClass = gSemesterTableCellCalendarCSSClassHTML.replace( "#ALTERNATECSSCOLUMN", alternateCSSRowString )
                if ( ( currentDate.weekday() == lecture1Day ) or ( currentDate.weekday() == lecture2Day ) ): # Lectures
                    labelString = labelString + lectures[whichLecture]
                    whichLecture = whichLecture + 1
                elif ( ( currentDate.weekday() == lab1Day1 ) or ( currentDate.weekday() == lab1Day2 ) or ( currentDate.weekday() == lab2Day1 ) or ( currentDate.weekday() == lab2Day2 ) ): # Labs
                    labelString = labelString + labs[whichLab]
                    whichLab = whichLab + 1
                if ( currentDate.weekday() == discussionDay ): # Discussions
                    labelString = labelString + discussions[whichDisc]
                    whichDisc = whichDisc + 1
            writeCell( fout, labelString, cssClass, 12, linkList, cellID = calendarMonthIDHack, title = calendarDayTitleHack, columnSpan = colspan, highlightBorder = doHighlight )
            currentDate = currentDate + datetime.timedelta( days = 1 )
        while ( currentDate.weekday() != 0 ): # Skip to next Monday
            if ( whatsDues.has_key( currentDate ) ): # FIXME: Repeat of above
                duesThisWeek.append( whatsDues[currentDate] )
            currentDate = currentDate + datetime.timedelta( days = 1 )
        # Due
        dueString = ""
        for duesThisWeek in duesThisWeek:
            dueString = dueString + "\r" + duesThisWeek[0] + "<br />" + duesThisWeek[1] + " at " + duesThisWeek[2]
        writeCell( fout, dueString, gSemesterTableCellCalendarCSSClassHTML.replace( "#ALTERNATECSSCOLUMN", alternateCSSRowString ), 12, linkList )
        whichWeek = whichWeek + 1
        fout.write( gTableRowSuffixHTML )

    fout.write( gTableSuffixHTML )
    fout.write( gSuffixHTML )
    fout.close()

    fin.close()

    if ( whichHoliday != len( holidays ) ):
        warning( "Fell short of " + str( len( holidays ) - whichHoliday ) + " holidays while generating: " + str( holidays[whichHoliday:] ) )
    if ( whichLecture != len( lectures ) ):
        for lecture in lectures[whichLecture:]:
            if ( len( lecture ) > 1 ):
                warning( "Fell short of " + str( len( lectures ) - whichLecture ) + " lectures while generating: " + str( lectures[whichLecture:] ) )
                break
    if ( whichLab != len( labs ) ):
        for lab in labs[whichLab:]:
            if ( len( lab ) > 1 ):
                warning( "Fell short of " + str( len( labs ) - whichLab ) + " labs while generating: " + str( labs[whichLab:] ) )
                break
    if ( whichDisc != len( discussions ) ):
        for discussion in discussions[whichDisc:]:
            if ( len( discussions ) > 1 ):
                warning( "Fell short of " + str( len( discussions ) - whichDisc ) + " discussions while generating: " + str( discussions[whichDisc:] ) )
                break

else:

    print "Skipping semester calendar..."

print "Finished!"

if ( gOpenResults ):
    if ( gGenerateWeekly ):
        os.system( "bbedit " + gWeeklyFileName + gOutputExtension )
    if ( gGenerateSemester ):
        os.system( "open " + gSemesterFileName + gOutputExtension )
