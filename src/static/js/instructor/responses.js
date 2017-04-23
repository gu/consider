var selectedCourse = $('#responses').data().course;

$('#courseSelector').on('change', function () {
    location.href = "/responses?course=" + this.value;
});

$('#assignmentSelector').on('change', function () {
    location.href = "/responses?course=" + selectedCourse + "&assignment=" + this.value;
});
