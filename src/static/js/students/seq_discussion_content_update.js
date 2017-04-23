var assignmentKey = $('#content-update').data().assignmentkey;

$('#seqDiscussionForm').submit(function (event) {
    event.preventDefault();

    // Update content of textarea(s) handled by CKEditor
    for ( instance in CKEDITOR.instances ) {
        CKEDITOR.instances[instance].updateElement();
    }

    var $form = $(this),
        url = $form.attr('action');
    $.post(url,
      {
          assignment: assignmentKey,
          text: $form.find('#seqDiscussionPost').val()
      },
      function (data) {
          if (data.charAt(0) == 'E') {
              bootbox.alert(data);
          } else {
              location.reload();
          }
      }
    );
});
