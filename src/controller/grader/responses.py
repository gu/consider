"""
responses.py
~~~~~~~~~~~~~~~~~
Implements the APIs for Grader control over student responses within the app.

- Author(s): Capstone team AU16

Refer to comments within /src/controller/grader/init.py for a better
understanding of the code for graders.

--------------------


"""

import webapp2
from google.appengine.api import users

from src import model, utils


class Responses(webapp2.RequestHandler):
    """
    API to retrieve and display responses for each assignment, tabbed into different rounds.
    """

    def get(self):
        """
        HTTP GET method to retrieve the responses.
        """
        # First, check that the logged in user is an grader
        grader = utils.check_privilege(model.Role.grader)
        if not grader:
            # Send them home and short circuit all other logic
            return self.redirect('/')
        # end

        # Create logout url
        logout_url = users.create_logout_url(self.request.uri)
        # And grab the course and assignment name from the page
        course_name = self.request.get('course')
        selected_assignment_name = self.request.get('assignment')
        # And grab all the other courses and assignments for this grader
        template_values = utils.get_template_all_courses_and_assignments(
            grader, course_name, selected_assignment_name)
        # Now check that the assignment from the webpage actually corresponded
        # to an actual assignment in this course, and that the template was set
        if 'selectedassignmentObject' in template_values:
            # If so, grab that assignment from the template values
            current_assignment = template_values['selectedassignmentObject']
            # And set the round
            template_values['round'] = current_assignment.rounds
            # Create a new dict for the responses
            resp = {}
            # And loop over the number of rounds (indexed at 1 for initial)
            for i in range(1, current_assignment.rounds + 1):
                # if seq. discussion and round==2, grab all the groups
                if not current_assignment.has_rounds and i == 2:
                    # extract all responses in each group
                    groups = model.Group.query(ancestor=current_assignment.key).fetch()
                    all_seq_responses = []
                    for g in groups:
                        seq_responses = model.SeqResponse.query(ancestor=g.key).order(model.SeqResponse.index).fetch()
                        all_seq_responses += seq_responses
                    template_values['seq_responses'] = all_seq_responses
                else:
                    round_i = model.Round.get_by_id(i, parent=current_assignment.key)
                    response = model.Response.query(ancestor=round_i.key).fetch()
                    # response is a list of all the responses for the round i
                    if response:
                        resp[str(i)] = response
                    # Add the responses to the template values
                    template_values['responses'] = resp
        # end
        # And set the template and render the page
        template_values['logouturl'] = logout_url
        from src import config
        template_values['documentation'] = config.DOCUMENTATION
        template = utils.jinja_env().get_template('grader/responses.html')
        self.response.write(template.render(template_values))
        # end get

# end class Responses
