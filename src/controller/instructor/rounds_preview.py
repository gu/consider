import datetime
import json

import jinja2
import webapp2
from google.appengine.api import users

from src import model, utils


class RoundsPreview(webapp2.RequestHandler):
    def get(self):
        print 'In Get'

    def post(self):
        print 'In Post'