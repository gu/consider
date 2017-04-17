import datetime
import json

import jinja2
import webapp2
import rounds
from google.appengine.api import users

from src import model, utils


class RoundsPreview(rounds.Rounds):

    def get(self):
        # First, check that the logged in user is an instructor
        instructor = utils.check_privilege(model.Role.instructor)
        if not instructor:
            # Redirect home if not an instructor
            return self.redirect('/home')
        # end

        # Otherwise, grab the key for the section
        course_name = self.request.get('course')
        section_key = self.request.get('section')
        # Make sure that it isn't null
        if not section_key:
            # Error if so, and redirect home
            utils.error('Section_key is null')
            self.redirect('/home')
        else:
            # And then grab the section from the key
            section = ndb.Key(urlsafe=section_key).get()
            # Making sure it's not null
            if not section:
                # Error if so
                utils.error('Section is null')
            else:
                # Now check if the current round is 0
                if section.current_round == 0:
                    # And redirect to an error if so
                    self.redirect('/error?code=103')
                else:
                    # Otherwise, we need to set our template values
                    self.render_template(instructor, section)

    # end get

    def post(self):
        print 'In Post'