var selectedCourse = $('#list-students').data().course;
var selectedassignment = $('#list-students').data().assignment;

$('#courseSelector').on('change', function () {
    location.href = "/students?course=" + this.value;
});

$('#assignmentSelector').on('change', function () {
    location.href = "/students?course=" + selectedCourse + "&assignment=" + this.value;
});

function addStudents() {
    $("#myModal").modal('show');
}

function submitStudents() {
    $("#modalForm").find('[type="submit"]').trigger('click');
}

$("#modalForm").submit(function (event) {
    //Prevent the default behaviour
    event.preventDefault();

    //collect form elements
    var $form = $(this),
            data = document.getElementById('student-data').value,
            email = document.getElementById('inputEmail').value,
            course = selectedCourse,
            assignment = selectedassignment,
            url = $form.attr("action");

    var emails = email.replace(/ /g, ',').split(/[\n,]+/);
    // Allows emails to be space, comma, and newline separated

    if(email != "") {
        email = email.split(",");
    }

    if(document.getElementById('student-data').value != "" || document.getElementById('inputEmail').value != "") {
        bootbox.confirm("Are you sure, you want to add " + (email.length + (((data.split(",").length) - 1) / 3)) + " student(s)?", function (result) {
            if(email != "" && data != "") {
                if (result) {
                    // do the POST and get the callback
                    $.post(url, {
                        emails: JSON.stringify(emails),
                        csv: JSON.stringify(data),
                        course: course,
                        assignment: assignment,
                        action: 'addBoth'
                    }, function (data) {
                        if (data.charAt(0) == 'E') {
                            bootbox.alert(data.substring(1));
                        }
                        else {
                            location.reload();
                        }
                    });
                }
            }
            else if(email != "") {
                if (result) {
                    // do the POST and get the callback
                    $.post(url, {
                        emails: JSON.stringify(emails),
                        course: course,
                        assignment: assignment,
                        action: 'add'
                    }, function (data) {
                        if (data.charAt(0) == 'E') {
                            bootbox.alert(data.substring(1));
                        }
                        else {
                            location.reload();
                        }
                    });
                }
            }
            else if(data != "") {
                if (result) {
                    // do the POST and get the callback
                    $.post(url, {
                        emails: JSON.stringify(data),
                        course: course,
                        assignment: assignment,
                        action: 'addCSV'
                    }, function (data) {
                        if (data.charAt(0) == 'E') {
                            bootbox.alert(data.substring(1));
                        }
                        else {
                            location.reload();
                        }
                    });
                }
            }
        });
    }
});

function deleteStudent(student) {
    bootbox.confirm("Are you sure, you want to remove student: " + student + "?", function (result) {
        if (result) {
            // do the POST and get the callback
            $.post("/students", {
                email: student,
                course: selectedCourse,
                assignment: selectedassignment,
                action: 'remove'
            }, function (data) {
                if (data.charAt(0) == 'E') {
                    bootbox.alert(data.substring(1));
                }
                else {
                    location.reload();
                }
            });
        }
    });
}
