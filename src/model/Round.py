from google.appengine.ext import ndb


class Question(ndb.Model):
    """
    .. _Question:

    An object to represent the Question in the data store. Currently only multiple choice questions are supported.
    """
    options_total = ndb.IntegerProperty(required=True, indexed=False)
    """ Integer. Number of options for the question. """
    question = ndb.StringProperty(required=True, indexed=False)
    """ String. The text of the question. """
    options = ndb.StringProperty(repeated=True, indexed=False)
    """ List of Strings. Options for this question."""
    # TODO Templates for questions - MCQ, long answers, short answers, etc.


class Round(ndb.Model):  # FIXME move under a Group?
    """
    .. _Round:

    An object to represent the Round in the datastore.

    Child of `Section`_.
    """
    deadline = ndb.DateTimeProperty(required=True, indexed=False)
    """ DateTime representation of the round end time. """
    number = ndb.IntegerProperty(required=True)
    """ Integer. Index of the round."""
    description = ndb.StringProperty(indexed=False)
    """ String. Description or brief instructions for the round."""
    is_quiz = ndb.BooleanProperty(default=False, indexed=False)
    """ Boolean. If ``True``, this is a quiz round (e.g., initial question); if ``False``, a discussion round."""
    quiz = ndb.StructuredProperty(Question, indexed=False)
    """ A `Question`_ property. Contains the question if this is a quiz round."""

    # NEW ATTRIBUTES FOR DYNAMIC ROUNDS: PART 1
    starttime = ndb.DateTimeProperty(required=True)
    """ DateTime representation of the round start time. """
    buffer_time = ndb.IntegerProperty(default=0, indexed=False)
    """ Integer. Represents the buffer time between rounds."""

    type = ndb.IntegerProperty(default=0, indexed=True)
    """ Type of the round. 1=initial question, 2=discussoin round, 3=sequential discussion round, 4=read only round, 5=final question"""

    @staticmethod
    def get_by_number(assignment_key, number):
        req_round = Round.query(ancestor=assignment_key).filter(Round.number == number).fetch(1)[0]
        return req_round if req_round else None

    @staticmethod
    def get_round_type(value):
        types = {'default': 0, 'initial': 1, 'discussion': 2, 'sequential': 3, 'readonly': 4, 'final': 5}
        return types[value] if types.has_key(value) else 0

    @staticmethod
    def fetch_real_rounds(assignment_key):
        rounds = [r for r in Round.query(ancestor=assignment_key).filter(Round.type != 4).fetch()]
        return rounds
