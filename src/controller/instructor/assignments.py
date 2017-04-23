"""
assignment.py
~~~~~~~~~~~~~~~~~
Implements the APIs for Instructor control of adding/removing assignments.

- Author(s): Rohit Kapoor, Swaroop Joshi, Tyler Rasor
- Last Modified: May 30, 2016

--------------------


"""
import webapp2

from src import model, utils


class assignments(webapp2.RequestHandler):
    """
    Handles requests for managing assignments: adding a assignment, toggling its status, etc.
    """

    def add_assignment(self, course, assignment_name):
        """
        Adds a assignment to the given course in the datastore.

        Args:
            course (object):
                Course to which the assignment is to be added.
            assignment_name (str):
                Name of the assignment; must be unique within the course.

        """
        # First, start by grabbing the assignment passed in from the database
        assignment = model.Assignment.get_by_id(assignment_name, parent=course.key)
        # Double check that it doesn't already exist
        if assignment:
            # And send an error if it does
            utils.error(assignment_name + ' already exists', handler=self)
        else:
            # Otherwise, create it, save it to the database, and log it
            assignment = model.Assignment(parent=course.key, id=assignment_name)
            assignment.name = assignment_name
            assignment.put()
            utils.log(assignment_name + ' added', type='Success!')
            # TODO Ask which assignment to copy from
            if course.recent_assignment:
                recent_assignment = model.Assignment.get_by_id(course.recent_assignment, parent=course.key)
                emails = [s.email for s in recent_assignment.students]
                from src.controller.instructor import Students
                Students.add_students(Students(self), assignment, emails)

    # end add_assignment

    def toggle_assignment(self, course, assignment_name):
        """
        Toggles the status of a assignment between Active and Inactive.

        Args:
            course (object):
                Course under which this assignment exists
            assignment_name (str):
                Name of the assignment to be toggled.

        """
        # First, start by grabbing the assignment from the passed in value
        _assignment = model.Assignment.get_by_id(assignment_name, parent=course.key)
        # Double check that it actually exists
        if _assignment:
            # Toggle the assignment to active, save it to the database, and log it
            _assignment.is_active = not _assignment.is_active
            _assignment.put()
            utils.log('Status changed for ' + assignment_name, type='Success!')
        else:
            # Send an error if the assignment passed in doesn't exist
            utils.error('assignment ' + assignment_name + ' not found', handler=self)
            # end

    # end toggle_assignment

    def post(self):
        """
        HTTP POST method to add a assignment to a course.
        """
        # First, check that the logged in user is an instructor
        instructor = utils.check_privilege(model.Role.instructor)
        if not instructor:
            # Send them home and short circuit all other logic
            return self.redirect('/')
        # end

        # Otherwise, grab the course, assignment, and action from the webpage
        course_name = self.request.get('course')
        assignment_name = self.request.get('assignment')
        action = self.request.get('action')
        # Double check that all three were supplied
        if not course_name or not assignment_name or not action:
            # Error if not
            utils.error('Invalid arguments: course_name or assignment_name or action is null', handler=self)
        else:
            # Otherwise, grab the course from the database
            course = model.Course.get_by_id(course_name.upper(), parent=instructor.key)
            # And check that it exists and is active
            if not course or not course.is_active:
                # Error if not
                utils.error(course_name + ' does not exist OR is not active!', handler=self)
            else:
                # Otherwise, switch on the action
                if action == 'add':
                    # Add a new assignment if action is add
                    self.add_assignment(course, assignment_name.upper())
                elif action == 'toggle':
                    # Or toggle
                    self.toggle_assignment(course, assignment_name.upper())
                else:
                    # Error if the action is neither toggle or add
                    utils.error('Unexpected action:' + action, handler=self)

    # end post

    def get(self):
        self.redirect('/courses')

        # end get

# end class assignment
