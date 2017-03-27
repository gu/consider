var selectedCourse = $('#list-students').data().course;
var selectedSection = $('#list-students').data().section;

$('#courseSelector').on('change', function () {
    location.href = "/students?course=" + this.value;
});

$('#sectionSelector').on('change', function () {
    location.href = "/students?course=" + selectedCourse + "&section=" + this.value;
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
            section = selectedSection,
            url = $form.attr("action");

    var emails = email.replace(/ /g, ',').split(/[\n,]+/);
    // Allows emails to be space, comma, and newline separated



    if(document.getElementById('student-data').value != "" || document.getElementById('inputEmail').value != "") {
        bootbox.confirm("Are you sure, you want to add " + (email.split(",").length + (((data.split(",").length) - 1) / 3)) + " student(s)?", function (result) {
            if(email != "" && email != "Email(s)") {
                if (result) {
                    // do the POST and get the callback
                    $.post(url, {
                        emails: JSON.stringify(email),
                        course: course,
                        section: section,
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
            if(data != "") {
                if (result) {
                    // do the POST and get the callback
                    $.post(url, {
                        emails: JSON.stringify(data),
                        course: course,
                        section: section,
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
                section: selectedSection,
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
