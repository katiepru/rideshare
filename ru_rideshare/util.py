import logging

from ru_rideshare.client import RideClient

def get_db_client(app, g):
  """Gets a reference to a RideClient for database operations.

  :Parameters:
    - `app`: A Flask application object.
    - `g`: Flask's magical global state object.

    :Returns:
      - A reference to a singleton RideClient.
  """

  if not hasattr(g, "client"):
    g.client = RideClient(host=app.config["DB_HOST"],
                          port=app.config["DB_PORT"],
                          passwd=app.config["DB_PASS"])
  return g.client

def set_logger(app):
  """Sets a logger with standard settings.

  :Parameters:
    - `app`: A Flask application object.
  """

  handler = logging.FileHandler(app.config["LOG_FILENAME"])
  handler.setLevel(logging.INFO)
  handler.setFormatter(app.config["LOG_FORMAT"])
  app.logger.addHandler(handler)
