from google.appengine.ext import ndb

from . import Section


class Student(ndb.Model):
    """
    .. _Student:

    An object to represent the Student in the app.
    """
    email = ndb.StringProperty(required=True)
    """ String. Must be non-empty and unique. Retrieved from Google automatically """
    sections = ndb.KeyProperty(kind=Section, repeated=True, indexed=False)
    """ List of active `Section`_ s this student is enrolled in. """
    first_name = ndb.StringProperty(required=False, default="")
    """Student's first name"""
    last_name = ndb.StringProperty(required=False, default="")
    """Student's last name"""
    alt_email = ndb.StringProperty(required=False, default="")
    """Student's alt_email name"""
