$('.sidebar-link > a').click(function() {
    var path = '/' + $(this).attr('dir');

    var selectedCourse = $('#courseSelector').val();
    var selectedSection = $('#sectionSelector').val();

    var params = {};
    if (path !== '/courses') {
        if (selectedCourse) {
            params.course = selectedCourse;
        }
        if (selectedSection) {
            params.section = selectedSection;
        }
        path += '?' + $.param(params);
        console.log(path);
    }
    window.location.href = path;
});