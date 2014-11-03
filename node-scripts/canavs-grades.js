// Upload grades from Pandagrader to bCourses


var Canvas = require('node-canvas-lms');
var fs = require('fs');
var path = require('path');

// Get Command Line Args
var args = process.argv;
var token = process.env.CANVAS_TOKEN;

// First two args are node and the script filename
if (args.length < 3) {
    console.log('PANDAGRADER UPLOADER: node canvas-grades.js <csv file> [canvas token]');
    process.exit(1);
}
if (!token & args.length < 4) {
    console.log('Please export the CANVAS_TOKEN variable or provide a token as input.');
    process.exit(1);
}

var gradesFile = path.resolve(process.cwd(), args[2]);

if (args[3]) {
    token = args[3];
}

// Specify encoding to return a string
var grades = fs.readFileSync(gradesFile, {encoding: 'utf8'});

var cs10 = new Canvas('https://bcourses.berkeley.edu', { token: token } );

var data = grades.split('\n');

// Create a 2D array.
for (var i = 0; i < data.length; i += 1) {
    data[i] = data[i].split(',');
}

var header = data[0];
var SCORE = 'Total Score';
var NAME  = 'Name';
var SID   = 'SID';

var scoreCol = header.indexOf(SCORE);
var nameCol  = header.indexOf(NAME);
var sidCol   = header.indexOf(SID);

var ASSIGNMENT_ID = '5179916'; // QUEST
var COURSE_ID     = '1246916'; // CS10 Fall 14


// Now post the grades....
// TODO: The extenstion students need a mapping like for lab checkoffs.
function postGrade(name, sid, score) {
    var scoreForm      = 'submission[posted_grade]=' + score,
        submissionBase = '/courses/' + COURSE_ID +
                         '/assignments/' + ASSIGNMENT_ID + '/submissions/',
        submissionPath = submissionBase + 'sis_user_id:',
        submissionALT  = submissionBase + 'sis_login_id:';

    // FIXME -- this is dumb.
    submissionPath += sid;
    submissionALT  += sid;

    cs10.put(submissionPath , '', scoreForm,
            callback(name, sid, score));
            
    // Access in SID and points in the callback
    function callback(name, sid, score) {
        return function(body) {
            // TODO: Make an error function
            // Absence of a grade indicates an error.
            // WHY DONT I CHECK HEADERS THATS WHAT THEY ARE FOR
            if (body.errors || !body.grade || body.grade != scoreForm) {
                // Attempt to switch to using sis_login_id instead of the sis_user_id
                // TODO: Make note about not finding sis_user_id and trying sis_login_id
                cs10.put(submissionALT , '', scoreForm,
                    loginCallback(name, sid, score));
            }
        };
    }
    
    // A modified call back for when sis_login_id is used
    // THese should really be condenced but I didn't want to figure
    // out a proper base case for a recursive callback...lazy....
    function loginCallback(name, sid, score) {
        return function(body) {
            var errorMsg = 'Problem encountered for ID: ' +
                            sid + ' NAME: ' + name;
            // TODO: Make an error function
            // Absence of a grade indicates an error.
            // WHY DONT I CHECK HEADERS THATS WHAT THEY ARE FOR
            if (body.errors || !body.grade || body.grade != score) {
                // Attempt to switch to using sis_login_id instead of the sis_user_id
                if (body.errors && body.errors[0]) {
                    errorMsg += '\nERROR:\t' + body.errors[0].message;
                }
                errorMsg += '\n' + 'Please enter the score directly in bCoureses.';
                errorMsg += '\n' + 'https://bcourses.berkeley.edu/courses/1246916/gradebook';
                console.log(errorMsg);
            }
        };
    }
}


// Post grades; skip header file
for (var i = 1; i < data.length; i += 1) {
    student = data[i];
    postGrade(student[nameCol], student[sidCol], student[scoreCol]);
}