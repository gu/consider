var selectedCourse = $('#group-responses-selectors').data().course;

$('#courseSelector').on('change', function () {
    location.href = "/group_responses?course=" + this.value;
});
$('#assignmentSelector').on('change', function () {
    location.href = "/group_responses?course=" + selectedCourse + "&assignment=" + this.value;
});
