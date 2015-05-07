""" RuRideshare - Rutgers University ridesharing application.

Implements database-level interactions for the ridesharing application.
"""

import datetime
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

        if port is None:
            port = 3306
        self._conn = oursql.connect(host=host, user=user, passwd=passwd, port=port,
                                db=db);


    def insert_driver(self, netid, name, car, seats):
        """Inserts a driver into the database

        :Parameters:
            - `netid`: the official Rutgers NetId of the driver
            - `name`: the full name of the driver
            - `car`: the type of car the driver uses
            - `seats: the numebr of seats the car has for passengers
        """

        print("Inserting a driver")
        curs = self._conn.cursor(oursql.DictCursor)
        curs.execute('INSERT INTO `drivers` (netid, name, car_type, seats)' \
                     ' VALUES (?, ?, ?, ?)', (netid, name, car, seats))


    def update_driver(self, netid, car, seats):
        """Updates a driver record if they get a new car

        :Parameters:
            - `netid`: the official Rutgers NetId of the driver
            - `car`: the type of car the driver uses
            - `seats: the numebr of seats the car has for passengers
        """

        curs = self._conn.cursor(oursql.DictCursor)
        curs.execute('UPDATE `drivers` SET car_type=?, seats=? WHERE netid=?',
                     (car, seats, netid))


    def is_driver(self, netid):
        """Checks is user is a driver.

        :Parameters:
            - `netid` : the official Rutgers NetId of the user

        Returns True if user is in the drivera table, False otherwise.
        """

        curs = self._conn.cursor(oursql.DictCursor)
        curs.execute('SELECT * FROM `drivers` WHERE netid=?', (netid,))

        for result in curs:
            #found a result
            return True
        return False



    def insert_request(self, rnetid, dtime, pickup, dest, seats, car):
        """Inserts a new ride request into the database

        :Parameters:
            - `rnetid`: the official Rutgers NetId of the requester
            - `dtime` : the date and time of pickup
            - `pickup` : a tuple containing the latitude and longitude
              coordinates of the pickup locations
            - `dest` : a tuple containing the latitude and longitude
              coordinates of the dropoff location
            - `seats` : the number of seats required
            - `car` : the preferred car type, or None if no preference
        """

        curs = self._conn.cursor(oursql.DictCursor)
        curs.execute('INSERT INTO `requests` (rnetid, dtime, pickup_lat, ' \
                     'pickup_long, dest_lat, dest_long, seats, car) VALUES ' \
                     '(?, ?, ?, ?, ?, ?, ?, ?)', (rnetid, dtime, pickup[0],
                     pickup[1], dest[0], dest[1], seats, car))


    def accept_request(self, dnetid, rid):
        """Record that a driver has accepted a request

        :Parameters:
            - `dnetid` : the official Rutgers NetId of the driver
            - `rid` : the unique id of the request
        """

        curs = self._conn.cursor(oursql.DictCursor)
        curs.execute('UPDATE `requests` SET driver=? WHERE id=?',
                     (dnetid, rid))


    def cancel_request(self, rid):
        """Removes a request from the database

        :Parameters:
            - `rid` : the id of the request to delete
        """

        curs = self._conn.cursor(oursql.DictCursor)
        curs.execute('DELETE FROM `requests` WHERE id=?', (rid,))


    def remove_driver_from_request(self, rid):
        """Removes the confirmed driver from a request

        :Parameters:
            - `rid` : the id of the request
            - `dnetid` : the official Rutgers NetId of the driver
        """

        curs = self._conn.cursor(oursql.DictCursor)
        curs.execute('UPDATE `requests` SET driver=NULL WHERE id=?', (rid,))


    def delete_past_requests(self):
        """Deletes all requests that started before right now """

        curs = self._conn.cursor(oursql.DictCursor)
        now = datetime.datetime.now()
        now_str = now.strftime('%Y-%m-%d')

        curs.execute('DELETE FROM `requests` WHERE dtime<?', (now_str,))


    def find_requests_in_x_miles(self, lat, lon, x):
        """Finds all requests within x miles of the given location

        :Parameters:
            - `lat` : latitude coordinate of given location
            - `lon` : longitude coordinate of given location
            - `x` : number of miles to search within
        """

        curs = self._conn.cursor(oursql.DictCursor)
        curs.execute('SELECT id FROM `requests` WHERE harvesine(?, ?, ' \
                           'pickup_lat, pickup_long)<?', (lat, lon, x))
        l = []
        for i in curs:
            l.append(i)
        return l


    def find_requests_in_x_mins(self, x):
        """Finds all requests with pickup times within x minutes from now.

        :Parameters:
            - `x` : number of minutes from now to search within
        """

        curs = self._conn.cursor(oursql.DictCursor)
        curs.execute('SELECT id FROM `requests` WHERE dtime BETWEEN ' \
                     'NOW() AND DATE_ADD(NOW(), INTERVAL ? MINUTE)', (x,))
        l = []
        for i in curs:
            l.append(i)
        return l


    def find_requests_in_mins_miles(self, lat, lon, miles, mins):
        """Finds all requests within x miles of the given location

        :Parameters:
            - `lat` : latitude coordinate of given location
            - `lon` : longitude coordinate of given location
            - `miles` : number of miles to search within
            - `mins` : number of minutes from now to search within
        """

        curs = self._conn.cursor(oursql.DictCursor)
        curs.execute('SELECT id FROM `requests` WHERE dtime BETWEEN ' \
                     'NOW() AND DATE_ADD(NOW(), INTERVAL ? MINUTE) ' \
                     'AND harvesine(?, ?, pickup_lat, pickup_long)<?',
                     (mins, lat, lon, miles))
        l = []
        for i in curs:
            l.append(i)
        return l
