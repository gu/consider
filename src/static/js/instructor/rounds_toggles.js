var selectedCourse = $('#rounds').data().course;

$('#courseSelector').on('change', function () {
        location.href = "/rounds?course=" + this.value;
});
$('#assignmentSelector').on('change', function () {
    location.href = "/rounds?course=" + selectedCourse + "&assignment=" + this.value;
});

// Toggle anonymity status on server
    function toggleAnon(course, assignment, anon) {
        bootbox.confirm("Toggle Anonymity?", function (result) {
            if (result) {
                console.log("result = " + result);
                $.post("/rounds", {course: course, assignment: assignment, action: 'toggle_anon'}, function (data) {
                    if (data.charAt(0) == 'E') {
                        bootbox.alert(data.substring(1));
                    } else {
                        location.href = "/rounds?course=" + course + "&assignment=" + assignment;
                    }
                });
            }
        });
    }
    function toggleRounds(course, assignment) {
        bootbox.confirm("Toggle Rounds-based structure?", function (result) {
            if (result) {
                console.log("result = " + result);
                $.post("/rounds", {
                    course: course,
                    assignment: assignment,
                    action: 'toggle_round_structure'
                }, function (data) {
                    if (data.charAt(0) == 'E') {
                        bootbox.alert(data.substring(1));
                    } else {
                        location.href = "/rounds?course=" + course + "&assignment=" + assignment;
                    }
                });
            }
        });
    }
