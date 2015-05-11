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



    def insert_request(self, rnetid, dtime, pickup, dest, seats, car, phone):
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
            - `phone` : the phone number of the requester
        """

        curs = self._conn.cursor(oursql.DictCursor)
        curs.execute('INSERT INTO `requests` (rnetid, dtime, pickup_lat, ' \
                     'pickup_long, dest_lat, dest_long, seats, car, phone) VALUES ' \
                     '(?, ?, ?, ?, ?, ?, ?, ?, ?)', (rnetid, dtime, pickup[0],
                     pickup[1], dest[0], dest[1], seats, car, phone))


    def accept_request(self, dnetid, rid):
        """Record that a driver has accepted a request

        :Parameters:
            - `dnetid` : the official Rutgers NetId of the driver
            - `rid` : the unique id of the request
        """

        curs = self._conn.cursor(oursql.DictCursor)
        curs.execute('UPDATE `requests` SET driver=? WHERE id=?',
                     (dnetid, rid))
        curs.execute('SELECT phone, dtime FROM `requests` WHERE id=?', (rid,))

        for i in curs:
            return (i['phone'], i['dtime'])


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


    def find_requests(self, a):
        """Finds all requests within some amount of miles of the pickup
        location, some amount of miles of the dropoff location, and some amount
        of time from a specified time.

        :Parameters:
            - `a["plat"]` : latitude coordinate of pickup location
            - `a["plon"]` : longitude coordinate of pickup location
            - `a["dlat"]` : latitude coordinate of dest location
            - `a["dlon"]` : longitude coordinate of dest location
            - `a["pmiles"]` : number of miles to search within from pickup
            - `a["dmiles"]` : number of miles to search within from dest
            - `a["mins"]` : number of minutes from now to search within
            - `a["time"]` : time to search from
            - `a["pickup"] : pickup address
            - `a["dest"] : dest address
        """
        curs = self._conn.cursor(oursql.DictCursor)
        where = ""
        tup = ()
        if a['time']:
            if a['pickup']:
                if a['dest']:
                    where = 'dtime BETWEEN ' \
                        '? AND DATE_ADD(?, INTERVAL ? MINUTE) ' \
                        'AND harvesine(?, ?, pickup_lat, pickup_long)<?' \
                        ' AND harvesine(?, ?, dest_lat, dest_long)<?'
                    tup = (a["time"], a["time"], a["mins"], a["plat"],
                           a["plon"], a["pmiles"], a["dlat"], a["dlon"],
                           a["dmiles"])
                else:
                    where = 'dtime BETWEEN ' \
                        '? AND DATE_ADD(?, INTERVAL ? MINUTE) ' \
                        'AND harvesine(?, ?, pickup_lat, pickup_long)<?'
                    tup = (a["time"], a["time"], a["mins"], a["plat"],
                           a["plon"], a["pmiles"])
            elif a['dest']:
                where = 'dtime BETWEEN ' \
                    '? AND DATE_ADD(?, INTERVAL ? MINUTE) ' \
                    'AND harvesine(?, ?, dest_lat, dest_long)<?'
                tup = (a["time"], a["date"], a["mins"], a["dlat"], a["dlon"],
                       a["dmiles"])
            else:
                where = 'dtime BETWEEN ' \
                    '? AND DATE_ADD(?, INTERVAL ? MINUTE)'
                tup = (a["time"], a["time"], a["mins"])
        else:
            if a['pickup']:
                if a['dest']:
                    where = 'harvesine(?, ?, pickup_lat, pickup_long)<?' \
                        ' AND harvesine(?, ?, dest_lat, dest_long)<?'
                    tup = (a["plat"], a["plon"], a["pmiles"], a["dlat"],
                           a["dlon"], a["dmiles"])
                else:
                    where = 'harvesine(?, ?, pickup_lat, pickup_long)<?'
                    tup = (a["plat"], a["plon"], a["pmiles"])
            else:
                where = 'harvesine(?, ?, dest_lat, dest_long)<?'
                tup = (a["dlat"], a["dlon"], a["dmiles"])


        curs.execute('SELECT * FROM `requests` WHERE ' + where + ' AND ' \
                     'driver is NULL', tup)


        l = []
        for i in curs:
            fixed = self.request_to_str(i)
            l.append(fixed)
        return l


    def request_to_str(self, res):
        res['pickup_long'] = float(res['pickup_long'])
        res['pickup_lat'] = float(res['pickup_lat'])
        res['dest_long'] = float(res['dest_long'])
        res['dest_lat'] = float(res['dest_lat'])
        res['dtime'] = res['dtime'].strftime("%Y-%m-%d %H:%M")
        return res;
