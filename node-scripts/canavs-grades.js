// Upload grades from Pandagrader to bCourses


var Canvas = require('node-canvas-lms').Canvas;
var fs = require('fs');
var path = require('path');

// Get Command Line Args
var args = process.argv;
var token = process.env.CANVAS_TOKEN;

// First two args are node and the script filename
if (args.length < 4) {
    console.log('GRADESCOPE UPLOADER: node canvas-grades.js <grades.csv> <assnID> [canvas token]');
    process.exit(1);
}
if (!token & args.length < 5) {
    console.log('Please export the CANVAS_TOKEN variable or provide a token as input.');
    process.exit(1);
}

var gradesFile = path.resolve(process.cwd(), args[2]);

var ASSIGNMENT_ID = args[3];
console.log('Uploading Scores for: ' + ASSIGNMENT_ID);

if (args[4]) {
    token = args[4];
}

// Specify encoding to return a string
var grades = fs.readFileSync(gradesFile, {encoding: 'utf8'});

var cs10 = new Canvas('https://bcourses.berkeley.edu', { token: token } );

var data = grades.split('\n');

// Create a 2D array.
for (var i = 0; i < data.length; i += 1) {
    data[i] = data[i].split(',');
}

// Must exactly match the CSV first row!
var header = data[0];
var SCORE = 'Total Score';
var NAME  = 'Name';
var SID   = 'SID';

var scoreCol = header.indexOf(SCORE);
var nameCol  = header.indexOf(NAME);
var sidCol   = header.indexOf(SID);

var COURSE_ID = '1301472'; // CS10 Spring 2015


// Now post the grades....
// TODO: The extenstion students need a mapping like for lab checkoffs.
function postGrade(name, sid, score, num) {
    var scoreForm      = 'submission[posted_grade]=' + score,
        submissionBase = '/courses/' + COURSE_ID +
                         '/assignments/' + ASSIGNMENT_ID + '/submissions/',
        submissionPath = submissionBase + 'sis_user_id:',
        submissionALT  = submissionBase + 'sis_login_id:';

    // FIXME -- this is dumb.
    submissionPath += sid;
    submissionALT  += sid;

    cs10.put(submissionPath , '', scoreForm,
            callback(name, sid, score, i));

    // Access in SID and points in the callback
    function callback(name, sid, score, i) {
        if (! (i % 15)) {
            console.log('Progress: ' + i + ' grades posted.');
        }
        return function(error, response, body) {
            // TODO: Make an error function
            // Absence of a grade indicates an error.
            // WHY DONT I CHECK HEADERS THATS WHAT THEY ARE FOR
            if (error || !body || body.errors) {
                var errorMsg = 'Problem: SID: ' + sid + ' NAME: ' + name +
                                ' SCORE: ' + score;
                if (error) {
                    console.log(error);
                }
                // Well, shit... just report error
                if (body && body.errors && body.errors[0]) {
                    errorMsg += '\nERROR:\t' + body.errors[0].message;
                }
                errorMsg += '\n\t' + submissionPath;
                console.log(errorMsg);
                // cs10.put(submissionALT , '', scoreForm,
//                     loginCallback(name, sid, score));
            }
        };
    }

    // A modified call back for when sis_login_id is used
    // THese should really be condenced but I didn't want to figure
    // out a proper base case for a recursive callback...lazy....
    function loginCallback(name, sid, score) {
        return function(error, response, body) {
            var errorMsg = 'Problem: SID: ' + sid + ' NAME: ' + name +
                           ' SCORE: ' + score;
           if (error || !body || body.errors || !body.grade || body.grade != score) {
                console.log(error);
                if (body && body.errors && body.errors[0]) {
                    errorMsg += '\nERROR:\t' + body.errors[0].message;
                }
                errorMsg += '\n\t' + submissionPath;
                console.log(errorMsg);
            }
        };
    }
}


// Post grades; skip header file
console.log('Posting ' + (data.length - 1) + ' grades.');
for (var i = 1; i < data.length; i += 1) {
    student = data[i];
    postGrade(student[nameCol], student[sidCol], student[scoreCol], i);
}