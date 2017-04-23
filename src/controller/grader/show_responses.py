import csv

import webapp2
from google.appengine.api import users

from src import model, utils

""" - Author(s): Capstone team AU16

Refer to comments within /src/controller/grader/init.py for a better
understanding of the code for graders.

"""

class ShowResponses(webapp2.RequestHandler):
    def get(self):
        # First, check that the logged in user is an grader
        grader = utils.check_privilege(model.Role.grader)
        if not grader:
            # Send them home and short circuit all other logic
            return self.redirect('/')
        # end

        # Otherwise, create a logout url
        logout_url = users.create_logout_url(self.request.uri)
        # And get the course and assignment names from the page
        course_name = self.request.get('course')
        selected_assignment_name = self.request.get('assignment')
        # Grab all the courses and assignments for the logged in grader
        template_values = utils.get_template_all_courses_and_assignments(grader,
                                                                      course_name.upper(),
                                                                      selected_assignment_name.upper())
        logout_url = users.create_logout_url(self.request.uri)
        template_values['logouturl'] = logout_url
        if 'selectedassignmentObject' in template_values:
            # If so, grab that assignment from the template values
            current_assignment = template_values['selectedassignmentObject']
            if current_assignment.students:
                # template_values['students'] = current_assignment.students
                template_values['num_std'] = len(current_assignment.students)
            if current_assignment.rounds:
                template_values['rounds'] = current_assignment.rounds
            if current_assignment.groups:
                template_values['num_group'] = current_assignment.groups
        from src import config
        template_values['documentation'] = config.DOCUMENTATION
        template = utils.jinja_env().get_template('grader/show_responses.html')
        self.response.write(template.render(template_values))


class DataExport(webapp2.RequestHandler):
    def post(self):
        course_name = self.request.get('course')
        assignment_name = self.request.get('assignment')
        selector = self.request.get('action')
        # print selector
        grader_tmp = utils.check_privilege(model.Role.grader)
        grader = model.Grader.get_by_id(grader_tmp.email)
        grader.export_course = course_name.upper()
        course = model.Course.get_by_id(course_name, parent=grader.key)
        course.export_assignment = assignment_name.upper()
        assignment = model.Assignment.get_by_id(assignment_name.upper(), parent=course.key)
        assignment.export_info = selector
        grader.put()
        course.put()
        assignment.put()
        # print ('finished')

    def get(self):
        self.response.headers['Content-Type'] = 'application/txt'
        # out = self.makeit()
        # self.response.write(out.getvalue())
        grader_tmp = utils.check_privilege(model.Role.grader)
        writer = csv.writer(self.response.out)
        grader = model.Grader.get_by_id(grader_tmp.email)
        course = model.Course.get_by_id(grader.export_course, parent=grader.key)
        assignment = model.Assignment.get_by_id(course.export_assignment, parent=course.key)
        students = assignment.students
        writer.writerow([grader.export_course, course.export_assignment, ])
        selector = assignment.export_info
        selector = selector.split()
        count = 0
        export_rounds = {}
        print selector
        while count < len(selector):
            if int(selector[count]) in export_rounds.keys():
                export_rounds[int(selector[count])].append(int(selector[count + 1]))
            else:
                export_rounds[int(selector[count])] = []
                export_rounds[int(selector[count])].append(int(selector[count + 1]))
            count += 2
        print export_rounds
        rounds = model.Round.query(ancestor=assignment.key).fetch()
        for i in export_rounds.keys():
            writer.writerow(['This is student ' + students[i].email + ' :', ])
            for j in export_rounds[i]:
                writer.writerow(['Round' + str(j), ])
                responses = model.Response.query(ancestor=rounds[j - 1].key).fetch()
                for resp in responses:
                    if resp.student == students[i].email:
                        # print 'test@@@'
                        writer.writerow([resp.student, resp.comment, resp.response, ])
        # writer.writerow([grader.export_course, course.export_assignment, grader.email, ])
        print 'Hello!'


class HtmlExport(webapp2.RequestHandler):
    def get(self):
        grader_tmp = utils.check_privilege(model.Role.grader)
        grader = model.Grader.get_by_id(grader_tmp.email)
        course = model.Course.get_by_id(grader.export_course, parent=grader.key)
        assignment = model.Assignment.get_by_id(course.export_assignment, parent=course.key)
        students = assignment.students
        selector = assignment.export_info
        selector = selector.split()
        count = 0
        export_rounds = {}
        # print selector
        while count < len(selector):
            if int(selector[count]) in export_rounds.keys():
                export_rounds[int(selector[count])].append(int(selector[count + 1]))
            else:
                export_rounds[int(selector[count])] = []
                export_rounds[int(selector[count])].append(int(selector[count + 1]))
            count += 2
        # print export_rounds
        rounds = model.Round.query(ancestor=assignment.key).fetch()
        template_values = {}
        output_students = []
        output_seq_rounds = {}
        output_options = {}
        output_comments = {}
        output_responses = {}
        output_summary = {}
        # export_rounds contain {key, value}, where key is student and value is round
        for i in export_rounds.keys():
            output_students.append(students[i])
            output_seq_rounds[students[i].email] = []
            output_options[students[i].email] = []
            output_comments[students[i].email] = []
            output_responses[students[i].email] = []
            output_summary[students[i].email] = []
            for j in export_rounds[i]:
                output_seq_rounds[students[i].email].append(j)
                flag = False
                if assignment.has_rounds:  # TODO Also for last and first round in seq
                    responses = model.Response.query(ancestor=rounds[j - 1].key).fetch()
                    for resp in responses:
                        utils.log('resp = ' + str(resp))
                        if resp.student == students[i].email:
                            output_options[students[i].email].append(resp.option)
                            output_comments[students[i].email].append(resp.comment)
                            output_responses[students[i].email].append(resp.response)
                            output_summary[students[i].email].append(resp.summary)
                            flag = True
                    if not flag:
                        output_options[students[i].email].append('NA')
                        output_comments[students[i].email].append('NA')
                        output_responses[students[i].email].append('NA')
                        output_summary[students[i].email].append('NA')
                else:
                    responses = model.SeqResponse.query(ancestor=rounds[j - 1].key).fetch()
                    utils.log('responses = ' + str(responses))
                    for resp in responses:
                        utils.log('resp = ' + str(resp))
                        if resp.author == students[i].email:
                            output_options[students[i].email].append('NA')
                            output_comments[students[i].email].append(resp.text)
                            output_responses[students[i].email].append('NA')
                            output_summary[students[i].email].append('NA')
                            flag = True
                        if not flag:
                            output_options[students[i].email].append('NA')
                            output_comments[students[i].email].append('NA')
                            output_responses[students[i].email].append('NA')
                            output_summary[students[i].email].append('NA')

        template_values['students'] = output_students
        template_values['seq_rounds'] = output_seq_rounds
        template_values['comments'] = output_comments
        template_values['responses'] = output_responses
        template_values['option'] = output_options
        template_values['summary'] = output_summary
        template = utils.jinja_env().get_template('grader/show_html_responses.html')
        self.response.write(template.render(template_values))
