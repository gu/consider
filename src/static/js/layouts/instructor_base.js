$('.sidebar-link > a').click(function() {
    var path = '/' + $(this).attr('dir');

    var selectedCourse = $('#courseSelector').val();
    var selectedAssignment = $('#assignmentSelector').val();

    var params = {};
    if (path !== '/courses') {
        if (selectedCourse) {
            params.course = selectedCourse;
        }
        if (selectedAssignment) {
            params.assignment = selectedAssignment;
        }
        path += '?' + $.param(params);
        console.log(path);
    }
    window.location.href = path;
});