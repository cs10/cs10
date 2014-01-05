// Constants for use by the script
var EMAIL_SENT = "EMAIL_SENT";
var READY      = "READY"
var SUBJ       = "CS10 Final Project Proposal Feedback";

function sendEmails() {
  var sheet    = SpreadsheetApp.getActiveSheet();
  var startRow = 2;  // First row of data to process
  var numRows  = 19;   // Number of rows to process
  // Fetch all of the cells.  30 Columns to include the aggregated info and an extra SENT field
  var dataRange = sheet.getRange(startRow, 1, numRows, 31)
  // Fetch values for each row in the Range.
  var data = dataRange.getValues();
  for (var i = 0; i < data.length; ++i) {
    var row = data[i];
    var address = row[2] + ", " + row[5] + ", " + row[8]; // Column C, F, I
    var message = "";
    message += "Hey everyone,\n\t Here's the feedback from your Final Project Proposal. Please send me a message if you have any questions, and make you're everyone on your team got the email. Thanks! \n\n Good Luck! :) \n Michael";
    // Genius idea, make the TA name be the TA field.
    message += "\n\n MY FEEDBACK:\n" + row[18]; //col S
    message += "\n\n For reference here is your submission:";
    message += "\n\nTeam Members: " + row[0] + ", " + row[3] + ", " + row[6]; // col ADG
    quest = [ "What is the overall goal of your project? How would your target audience use it?", "Individual Feature 1", "Individual Feature 2", "Individual Feature 3", "Describe why you think this project is sufficiently badass.", "At a high level, describe how you will implement your project.", "What will the group portion be?", "Will you be using hardware?", "Do you expect extra credit for this project?"];
    for (var j = 0; j < quest.length; j++) {
      message += "\n\n" + quest[j] + "\n\t" + row[j+9];
    }
    MailApp.sendEmail(address, SUBJ, message);
  }
}