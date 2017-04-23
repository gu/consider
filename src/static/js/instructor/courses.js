$("#modalForm").submit(function (event) {
    //Prevent the default behaviour
    event.preventDefault();

    //collect form elements
    var $form = $(this),
            courseName = $('#courseName').val();

    bootbox.confirm("Are you sure, you want to add " + courseName + " ?", function (result) {
        if (result) {
            // do the POST and get the callback
            $.post("/courses", {name: courseName, action:'add'}, function (data) {
                if (data.charAt(0) == 'E') {
                    $("#courseNameContainer").addClass("has-error");
                    $("#courseNameHelpBlock").text(data.substring(1));
                    $("#courseName").focus();
                }
                else {
                    location.reload();
                }
            });
        }
    });
});

$("#assignmentModalForm").submit(function (event) {
    //Prevent the default behaviour
    event.preventDefault();

    //collect form elements
    var $form = $(this),
            assignmentName = $('#assignmentName').val(),
            assignmentCourse = $('#assignmentCourse').val(),
            url = $form.attr("action");

    bootbox.confirm("Are you sure, you want to add assignment: " + assignmentName + " to Course: " + assignmentCourse + "  ?", function (result) {
        if (result) {
            // do the POST and get the callback
            $.post('/assignments', {assignment: assignmentName, course: assignmentCourse, action: 'add'}, function (data) {
                if (data.charAt(0) == 'E') {
                    $("#assignmentNameContainer").addClass("has-error");
                    $("#assignmentNameHelpBlock").text(data.substring(1));
                    $("#assignmentName").focus();
                }
                else {
                    location.href = "/home?course=" + assignmentCourse;
                }
            });
        }
    });
});

$(document).ready(function () {
    $('#courseName').tooltip({'trigger': 'focus', 'title': 'Course name should be unique'});
    $('#assignmentName').tooltip({'trigger': 'focus', 'title': 'assignment name should be unique inside a Course'});
});

function submitCourse() {
    $("#modalForm").find('[type="submit"]').trigger('click');
}

function submitassignment() {
    $("#assignmentModalForm").find('[type="submit"]').trigger('click');
}

function addCourse() {
    $("#myModal").modal('show');
}

$('#myModal').on('shown.bs.modal', function () {
    $('#courseName').focus();
});

$('#assignmentModal').on('shown.bs.modal', function () {
    $('#assignmentName').focus();
});

function addassignment(course) {
    $("#assignmentModal").modal('show');
    $("#assignmentCourse").val(course);
}

function toggleCourseStatus(course) {
    bootbox.confirm("Toggle status of course: " + course + "?", function (result) {
        if (result) {
            // do the POST and get the callback
            $.post("/courses",
            {
              name: course,
              action:'toggle'
            },
            function () {
              location.href = "/home?course=" + course;
            });
        }
    });
}

function toggleassignmentStatus(course, assignment) {
    bootbox.confirm("Toggle status of: " + assignment + " in course: " + course + "?", function (result) {
        if (result) {
            // do the POST and get the callback
            $.post("/assignments",
            {
              course: course,
              assignment: assignment,
              action:'toggle'
            },
            function (data) {
              if (data.charAt(0) == 'E') {
                  bootbox.alert(data.substring(1));
              }
              else {
                  location.href = "/home?course=" + course;
              }
            });
        }
    });
}
