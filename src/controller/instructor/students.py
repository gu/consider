"""
students.py
~~~~~~~~~~~~~~~~~
Implements the APIs for Instructor control of adding/removing students.

- Author(s): Rohit Kapoor, Swaroop Joshi, Tyler Rasor
- Last Modified: May 30, 2016

--------------------


"""
import json

import webapp2
from google.appengine.api import users

from src import model, utils


class Students(webapp2.RequestHandler):
    """
    API to add a student to the given assignment and course.
    """

    def add_students(self, assignment, emails):
        """
        Adds one or more students to the given assignment in the datastore.

        Args:
            assignment (object):
                assignment to which the studetns are to be added.
            emails (list):
                Emails (IDs) of students to be added.

        """
        # Start by looping over the list of emails supplied
        for email in emails:
            # Transform the supplied email to lowercase
            email = email.lower()
            # Then make a list of all the emails currently in the assignment
            student_emails = [s.email for s in assignment.students]
            # Check that the supplied email isn't already in the assignment
            if email not in student_emails:
                # And add them to the list of students for the assignment
                info = model.StudentInfo()
                info.email = email
                assignment.students.append(info)
            # end
            # Now grab the student from the database
            student = model.Student.get_by_id(email)
            # And if they don't already have a db entry
            if not student:
                # Create a new student and assign the email address
                student = model.Student(id=email)
                student.email = email
            # end
            # Now check if the current student is subscribed to this assignment
            if assignment.key not in student.assignments:
                # And add them if they weren't already
                student.assignments.append(assignment.key)
            # end
            # Save the student data back to the database
            student.put()
        # end
        # Now save all the assignment data back to the database and log it
        assignment.put()
        utils.log('Students added to assignment ' + str(assignment), type='Success!')

    # end add_students

    def add_studentsCSV(self, assignment, csv):
        """
        Adds one or more students to the given assignment in the datastore.

        Args:
            assignment (object):
                assignment to which the studetns are to be added.
            emails (list):
                Emails (IDs) of students to be added.

        """
        students = csv.split("\n")

        # Start by looping over the list of emails supplied
        for student in students:
            # Transform the supplied email to lowercase
            student = student.split(",")
            fname = student[0]
            lname = student[1]
            email = student[2]
            osu_email = student[3]

            # Then make a list of all the emails currently in the assignment
            student_emails = [s.email for s in assignment.students]
            # Check that the supplied email isn't already in the assignment
            if email not in student_emails:
                # And add them to the list of students for the assignment
                info = model.StudentInfo()
                info.email = email
                info.first_name = fname
                info.last_name = lname
                info.osu_email = osu_email
                assignment.students.append(info)
            # end
            # Now grab the student from the database
            student = model.Student.get_by_id(email)
            # And if they don't already have a db entry
            if not student:
                # Create a new student and assign the email address
                student = model.Student(id=email)
                student.email = email
                student.first_name = fname
                student.last_name = lname
                student.osu_email = osu_email
            # end
            # Now check if the current student is subscribed to this assignment
            if assignment.key not in student.assignments:
                # And add them if they weren't already
                student.assignments.append(assignment.key)
            # end
            # Save the student data back to the database
            student.put()

        # end
        # Now save all the assignment data back to the database and log it

        assignment.put()
        utils.log('Students added to assignment ' + str(assignment), type='Success!')

    def add_studentsBoth(self, assignment, emails, csv):
        """
        Adds one or more students to the given assignment in the datastore.

        Args:
            assignment (object):
                assignment to which the studetns are to be added.
            emails (list):
                Emails (IDs) of students to be added.

        """
        for email in emails:
            # Transform the supplied email to lowercase
            email = email.lower()
            # Then make a list of all the emails currently in the assignment
            student_emails = [s.email for s in assignment.students]
            # Check that the supplied email isn't already in the assignment
            if email not in student_emails:
                # And add them to the list of students for the assignment
                info = model.StudentInfo()
                info.email = email
                assignment.students.append(info)
            # end
            # Now grab the student from the database
            student = model.Student.get_by_id(email)
            # And if they don't already have a db entry
            if not student:
                # Create a new student and assign the email address
                student = model.Student(id=email)
                student.email = email
            # end
            # Now check if the current student is subscribed to this assignment
            if assignment.key not in student.assignments:
                # And add them if they weren't already
                student.assignments.append(assignment.key)
            # end
            # Save the student data back to the database
            student.put()
        # end
        # Now save all the assignment data back to the database and log it

        students = csv.split("\n")

        # Start by looping over the list of emails supplied
        for student in students:
            # Transform the supplied email to lowercase
            student = student.split(",")
            fname = student[0]
            lname = student[1]
            email = student[2]
            osu_email = student[3]

            # Then make a list of all the emails currently in the assignment
            student_emails = [s.email for s in assignment.students]
            # Check that the supplied email isn't already in the assignment
            if email not in student_emails:
                # And add them to the list of students for the assignment
                info = model.StudentInfo()
                info.email = email
                info.first_name = fname
                info.last_name = lname
                info.osu_email = osu_email
                assignment.students.append(info)
            # end
            # Now grab the student from the database
            student = model.Student.get_by_id(email)
            # And if they don't already have a db entry
            if not student:
                # Create a new student and assign the email address
                student = model.Student(id=email)
                student.email = email
                student.first_name = fname
                student.last_name = lname
                student.osu_email = osu_email
            # end
            # Now check if the current student is subscribed to this assignment
            if assignment.key not in student.assignments:
                # And add them if they weren't already
                student.assignments.append(assignment.key)
            # end
            # Save the student data back to the database
            student.put()

        # end
        # Now save all the assignment data back to the database and log it

        assignment.put()
        utils.log('Students added to assignment ' + str(assignment), type='Success!')

    # end add_students

    def remove_student(self, assignment, email):
        """
        Removes a specific students from the given assignment.

        Args:
            assignment (object):
                assignment from which the student is to be removed.
            email (str):
                Email (ID) of the student to be removed.

        """
        # First, grab the student from the db by the email passed in
        student = model.Student.get_by_id(email)
        # Check that there is actually a record for that email
        if not student:
            # And error if not
            utils.error('Student does not exist!', handler=self)
        else:
            # Create a new list for the assignment removing the student
            assignment.students = [s for s in assignment.students if s.email != email]  # TODO better? use remove?
            # Check if the student is enrolled in this assignment
            if assignment.key in student.assignments:
                # And remove them if so
                student.assignments.remove(assignment.key)
            # end
            # And save both the student and assignment back to the db and log it
            student.put()
            assignment.put()
            utils.log(
                'Student {0} has been removed from assignment {1}'.format(str(student),
                                                                       str(assignment)), handler=self, type='Success!')
            # end

    # end remove_student

    def post(self):
        """
        HTTP POST method to add the student.
        """
        # First, check that the logged in user is an instructor
        instructor = utils.check_privilege(model.Role.instructor)
        if not instructor:
            # Send them home and short circuit all other logic
            return self.redirect('/')
        # end

        # So first we need to get at the course and assignment
        course, assignment = utils.get_course_and_assignment_objs(self.request, instructor)
        # And grab the action from the page
        action = self.request.get('action')
        # Check that the action was actually supplied
        if not action:
            # Error if not
            utils.error('Invalid arguments: course_name or assignment_name or actoin is null', handler=self)
        else:
            # Now switch on the action
            if action == 'add':
                # Grab a list of the emails from the page
                emails = json.loads(self.request.get('emails'))
                # And create new students from that list
                self.add_students(assignment, emails)
            elif action == 'addCSV':
                # Grab a list of the emails from the page
                emails = json.loads(self.request.get('emails'))
                # And create new students from the list
                self.add_studentsCSV(assignment, emails)
            elif action == 'addBoth':
                # Grab a list of the emails from the page
                emails = json.loads(self.request.get('emails'))
                csv = json.loads(self.request.get('csv'))
                # And create new students from the list
                self.add_studentsBoth(assignment, emails, csv)
            elif action == 'remove':
                # Grab the email from the page to remove
                email = self.request.get('email').lower()
                # And remove it
                self.remove_student(assignment, email)
            else:
                # Send an error if any other action is supplied
                utils.error('Unexpected action: ' + action, handler=self)
                # end
                # end

    # end post

    def get(self):
        """
        HTTP GET method to retrieve the list of students from the datastore.
        """
        # First, check that the logged in user is an instructor
        instructor = utils.check_privilege(model.Role.instructor)
        if not instructor:
            # Send them home and short circuit all other logic
            return self.redirect('/')
        # end

        # Otherwise, create a logout url
        logout_url = users.create_logout_url(self.request.uri)
        # Get the course and assignment name from the webpage
        course_name = self.request.get('course')
        selected_assignment_name = self.request.get('assignment')
        # And start building the template values
        template_values = utils.get_template_all_courses_and_assignments(instructor, course_name.upper(),
                                                                      selected_assignment_name.upper())
        template_values['logouturl'] = logout_url
        from src import config
        template_values['documentation'] = config.DOCUMENTATION
        # Set the template and render the page
        template = utils.jinja_env().get_template('instructor/list_students.html')
        self.response.write(template.render(template_values))
        # end get

# end class Students
