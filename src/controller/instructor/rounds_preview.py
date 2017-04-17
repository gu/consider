import datetime
import json

import jinja2
import webapp2
import rounds
from google.appengine.api import users
from google.appengine.ext import ndb

from src import model, utils


class RoundsPreview(webapp2.RequestHandler):

    def get(self):
        """
        HTTP GET method to retrieve the rounds.
        """
        # First, check that the logged in user is an instructor
        instructor = utils.check_privilege(model.Role.instructor)
        if not instructor:
            # Send them home and short circuit all other logic
            return self.redirect('/')
        # end

        # Now create a logout url
        logout_url = users.create_logout_url(self.request.uri)
        # Grab the course and section name from the webpage
        course_name = self.request.get('course')
        selected_section_name = self.request.get('section')
        # And get all the courses and sections for this instructor
        template_values = utils.get_template_all_courses_and_sections(instructor, course_name.upper(),
                                                                      selected_section_name.upper())
        # Add the name of the current/local timezone to the template.
        template_values['tz'] = utils.tzname()
        # Now check that the section from the webpage actually corresponded
        # to an actual section in this course, and that the template was set
        if 'selectedSectionObject' in template_values:
            # If so, grab that section from the template values
            current_section = template_values['selectedSectionObject']
            # Set the current active round
            template_values['activeRound'] = 0
            # Send the current time stamp back to the view to do comparisons with
            template_values['now'] = datetime.datetime.now()
            # And grab all the rounds for this section
            # rounds = model.Round.query(ancestor=current_section.key).filter(model.Round.type != 4).fetch()
            rounds = model.Round.fetch_real_rounds(current_section.key)
            # Double check that there are actually rounds already created
            if rounds:
                # And set the template values
                template_values['rounds'] = rounds
                # Create an empty list to hold the discussion rounds
                discussion_rounds = []
                # And loop over all of the rounds for this section
                for r in rounds:
                    # Set the initial question
                    if r.number == 1:
                        template_values['initialQuestion'] = r
                    elif r.is_quiz:
                        # And if not the lead-in question, but still a quiz
                        # it must be the summary round
                        template_values['summaryQuestion'] = r
                    else:
                        # Otherwise, it's just a discussion round
                        discussion_rounds.append(r)
                        # end
                # end
                # Set the discussion round template values
                template_values['discussionRounds'] = discussion_rounds
            # end
            template_values['anon'] = current_section.is_anonymous
            template_values['round_structure'] = current_section.has_rounds

            # Check to see if the summary round was set in the template
            if 'summaryQuestion' in template_values:
                # If so, set the next round to the total number of rounds
                template_values['nextRound'] = current_section.rounds
            else:
                # Otherwise, it must be set to the number of rounds plus
                # one (to account for the eventual summary round)
                template_values['nextRound'] = current_section.rounds + 1
                # end
        # end
        # Set the template and render the page
        template_values['logouturl'] = logout_url
        from src import config
        template_values['documentation'] = config.DOCUMENTATION
        template = utils.jinja_env().get_template('../../templates/students/round.html')
        template.render_template(template_values)
        # end get

    def post(self):
        print 'In Post'

    def render_template(self, instructor, section):

        # update the database to the current round based on time
        database_round = utils.get_current_round(section)
        # Get the requested round number from the page
        current_round = self.request.get('round')
        # Now check that the round number passed in actually exists, and set
        # the requested round number appropriately if not
        if current_round:
            requested_round_number = int(current_round)
        else:
            requested_round_number = section.current_round
        # end

        # Grab the requested round
        requested_round = model.Round.get_by_id(requested_round_number, parent=section.key)
        # And check that it's not null
        if not requested_round:
            # Error if so
            self.redirect('/error?code=104')
        else:
            # Otherwise we need to set up our template values, create empty dict
            template_values = {}
            # Grab the deadline from the requested round
            deadline = requested_round.deadline
            # And the current time
            current_time = datetime.datetime.now()
            # And check if we're dealing with an expired round
            if deadline < current_time or requested_round_number < section.current_round:
                # Set the template value if so
                template_values['expired'] = True
            # end
            # Check if we're on the last round
            if requested_round.is_quiz and requested_round_number > 1:
                template_values['last_round'] = True
            # end
            # Now, just grab all the other generic values we need directly
            # template_values['deadline'] = datetime.datetime.strptime(requested_round.deadline, '%Y-%m-%dT%H:%M')
            template_values['deadline'] = requested_round.deadline
            template_values['sectionKey'] = self.request.get('section')
            template_values['rounds'] = section.current_round
            template_values['num_total_rounds'] = section.rounds
            template_values['show_name'] = not section.is_anonymous

            # Send round names
            if section.has_rounds:
                if section.rounds > 3:
                    disc_round_names = ['Round ' + str(i) for i in range(1, section.rounds - 2)] + ['Latest Posts']
                else:
                    disc_round_names = ['Round 1']
            else:
                disc_round_names = ['Discussion']

            round_names = ['Initial Submission'] + disc_round_names + ['Final Submission']
            template_values['round_names'] = round_names

            logout_url = users.create_logout_url(self.request.uri)
            template_values['logouturl'] = logout_url
            from src import config
            template_values['documentation'] = config.DOCUMENTATION
            template_values['curr_page'] = requested_round_number

            # Now we need to check if it's the initial or summary question
            if requested_round.is_quiz:
                # And set template values for quiz round
                self.quiz_view_template(instructor, requested_round, template_values)
                # And set the right template
                template = utils.jinja_env().get_template('students/round.html')
            else:
                # Otherwise, set up template values for appropriate discussion round
                if section.has_rounds:
                    self.discussion_view_template(instructor, section, requested_round_number, template_values)
                    # And set the right template
                    template = utils.jinja_env().get_template('students/discussion.html')
                else:
                    self.seq_discussion_view_template(instructor, section, template_values)
                    template_values['description'] = requested_round.description
                    template = utils.jinja_env().get_template('students/seq_discussion.html')
            # end
            # Now, render it.
            self.response.write(template.render(template_values))
            # end

            # end render_templates

    def quiz_view_template(student, rround, template_values):

        # Now set the remaining template values directly
        template_values['question'] = rround.quiz.question
        template_values['options'] = rround.quiz.options
        template_values['number'] = rround.quiz.options_total

    def seq_discussion_view_template(self, instructor, section, template_values):
        student_info = utils.get_student_info(instructor.email, section.students)
        if student_info:
            # 1. Grab student's alias and group from db
            template_values['alias'] = student_info.alias
            group_id = student_info.group
            group = model.Group.get_by_id(group_id, parent=section.key)
            if group:
                # 2. Extract all the posts in that group from db
                posts = model.SeqResponse.query(ancestor=group.key).order(model.SeqResponse.index).fetch()
                utils.log('Posts: ' + str(posts))
                # 3. Send all the posts to the template
                template_values['posts'] = posts

                # 4. Grab all posts from the previous round (initial)
                initial = model.Round.get_by_id(1, parent=section.key)
                initial_answers, did_not_participate = self.group_comments(group, section, initial)
                template_values['initial_answers'] = initial_answers
                template_values['did_not_participate'] = did_not_participate

    # end seq_discussion_view_template

    # end seq_discussion_view_template

    def discussion_view_template(self, instructor, section, round_number, template_values):
        student_info = utils.get_student_info(instructor.email, section.students)
        if student_info:
            template_values['alias'] = student_info.alias
            group_id = student_info.group
            group = model.Group.get_by_id(group_id, parent=section.key)
            # Double check that it was found
            if group:
                # Depending on round number, we have to grab from
                if round_number == 1:
                    previous_round = model.Round.get_by_id(1, parent=section.key)
                else:
                    previous_round = model.Round.get_by_id(round_number - 1, parent=section.key)
                # end
                # Now grab all the group comments for the previous round
                comments, did_not_participate = self.group_comments(group, section, previous_round)
                # Set the template value for all the group comments
                template_values['comments'] = comments
                template_values['did_not_participate'] = did_not_participate
                # Grab the requested round
                requested_round = model.Round.get_by_id(round_number, parent=section.key)
                # Grab the discussion description
                template_values['description'] = requested_round.description
                # And grab the logged in student's response
                stu_response = model.Response.get_by_id(instructor.email, parent=requested_round.key)
                # Check that they actually answered
                if stu_response:
                    # And set template values to show their previous response
                    template_values['comment'] = stu_response.comment
                    utils.log('Comment = {0}'.format(str(stu_response.comment)))
                    template_values['response'] = ','.join(str(item) for item in stu_response.response)

                    # end discussion_view_template


    def group_comments(group, section, previous_round):
        # Init an empty list for holding the comments
        comments = []
        did_not_participate = []
        # Now loop over the members in the group
        for student_email in group.members:
            # Grab each response from the previous round
            response = model.Response.get_by_id(student_email, parent=previous_round.key)

            # Get the student's info
            s = section.find_student_info(student_email)

            if response:
                comment = {
                    'alias': s.alias, 'email': s.email,
                    'response': response.comment, 'opinion': response.response
                }
                # Get thumbs if they exist
                if response.thumbs:
                    _thumbs = []
                    for _email, _value in response.thumbs.iteritems():
                        s_info = section.find_student_info(_email)
                        name = s_info.alias if s_info and section.is_anonymous else _email
                        _thumbs.append((name, _value))  # Add as a tuple
                    comment['thumbs'] = sorted(_thumbs)  # Send as sorted tuples

                # If the response has an associated option
                if response.option and response.option != 'NA':
                    # Grab the option
                    utils.log('response.option = ' + str(response.option))
                    opt = int(response.option[-1]) - 1
                    comment['option'] = previous_round.quiz.options[opt]
                else:
                    comment['option'] = ''  # default

                # And finally add the comment to the list
                comments.append(comment)
            else:
                # Else note down who did not participate
                name = s.alias if section.is_anonymous else s.email
                did_not_participate.append(name)

        utils.log('Comments = ' + str(comments))
        return comments, sorted(did_not_participate)