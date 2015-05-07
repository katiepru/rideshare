from flask import g
from flask_login import UserMixin, current_user
from flask_auth import LoginForm
from wtforms import TextField, PasswordField, validators

from ru_rideshare.app import app
from ru_rideshare.util import get_db_client

class User(UserMixin):
    """A User object used for logging in."""
    def __init__(self, netid, driver):
        self.netid = netid
        self.id = netid
        self.driver = driver

    def is_active(self):
        # return not self.client.is_blacklisted(self.netid)
        return True

    def __str__(self):
        """Returns the NetID of this user."""
        return self.netid

    def __repr__(self):
        """Returns the NetID of this user."""
        return self.netid


def get_user(fields):
    """Gets a user object from fields.
    :Returns:
    A User object from the username extracted from the argument.
    """
    # Check if user is driver
    client = get_db_client(app, g)
    d = client.is_driver(fields['username'])
    return User(fields['username'], d)
