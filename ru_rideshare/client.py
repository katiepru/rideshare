""" RuRideshare - Rutgers University ridesharing application.

Implements database-level interactions for the ridesharing application.
"""

import datetime
import random
import string

import oursql

class RideClient(object):
  """A class for database interactions"""

  def __init__(self, host=None, port=None, user="rideshare", passwd=None,
               db="rideshare"):
    """Create a new client connection.

    This client uses MariaDB. No network traffic occurs until a database
    method is called.

    :Parameters:
      - `host` (optional): the hostname to connect to; default to "localhost"
      - `port` (optional): the port to connection to on the server; defaults
          to the database default if not present
      - `user` (optional): the user to connect as; defaults to "rideshare"
      - `passwd` (optional): the password to use; defaults to None
      - `db` (optional): the database to use; defaults to "rideshare"
    """

    self._conn = oursql.connect(host=host, user=user, passwd=passwd, port=port,
                                db=db);

  def add_user(self, username):
    """Adds a new user to the users table.

    :Parameters:
      - `username`: the login username
    """

    curs = self._conn.cursor(oursql.DictCursor)
    return curs.execute('INSERT INTO `users` VALUES (?);' (username))

  def user_exists(self, username):
    curs = self._conn.cursor(oursql.DictCursor)
    res = curs.execute('SELECT * FROM `users` WHERE `username` = ?' (username))

  def insert_ride(self, username, pickup, dropoff, time):
      pass
