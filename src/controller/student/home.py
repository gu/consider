"""
home.py
~~~~~~~~~~~~~~~~~
Implements the APIs for Student homepage in the app.

- Author(s): Rohit Kapoor, Swaroop Joshi
- Last Modified: May 27, 2016

--------------------


"""

import webapp2
from google.appengine.api import users

from src import model, utils


class HomePage(webapp2.RequestHandler):
    def get(self):
        """
        Display a list of active ``assignment``_\ s this ``Student``_ is enrolled in.
        """
        # First, check that the logged in user is a student
        student = utils.check_privilege(model.Role.student)
        if not student:
            # Redirect home if not a student
            return self.redirect('/')
        # end

        # Create a url for the user to logout
        logout_url = users.create_logout_url(self.request.uri)
        students = [student]
        # Set up the template
        from src import config
        template_values = {
            'documentation': config.DOCUMENTATION,
            'logouturl': logout_url,
            'nickname': student.email
        }
        # Grab the assignments the student is a part of
        assignments = student.assignments
        # Create a new list for holding the assignment objects from the db
        assignment_list = []
        # Double check that the student is actually enrolled in a assignment
        if assignments:
            # Loop over all the assignments they're in
            for assignment in assignments:
                # Grab it from the db
                assignment_obj = assignment.get()
                if assignment_obj.is_active:
                    # Get the parent course for the assignment
                    course_obj = assignment.parent().get()
                    # Double check that both exist
                    if assignment_obj and course_obj:
                        # Grab the assignment key, assignment name, and course name
                        sec = {
                            'key': assignment.urlsafe(),
                            'name': assignment_obj.name,
                            'course': course_obj.name,
                            'group': findGroupIDByEmail(assignment_obj, student.email),
                            'round': utils.get_current_round(assignment_obj)
                        }
                        # And throw it in the list
                        assignment_list.append(sec)
                        # end
                        # end
        # end
        # Add the list of assignments the student is in to our template
        template_values['assignments'] = assignment_list
        # Set the template html page
        template = utils.jinja_env().get_template('students/home.html')
        # And render it
        self.response.write(template.render(template_values))
        # end get



# end class HomePage

def findGroupIDByEmail(assignment, email):
    for student in assignment.students:
        if student.email == email:
            return student.group
