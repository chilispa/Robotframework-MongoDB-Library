from __future__ import print_function

import robot
import robot.utils
from pymongo import MongoClient

from robot.libraries.BuiltIn import BuiltIn


class MongoConnectionManager(object):
    """
    Connection Manager handles the connection & disconnection to the database.
    """

    def __init__(self):
        """
        Initializes _dbconnection to None.
        """
        self._cache = robot.utils.ConnectionCache('No connection created')
        self._builtin = BuiltIn()

    def _push_cache(self, alias=None, connection=None):
        """
         Overlay _cache.register using dictionary
         Create a dictionary that contains the dbconnection and the api_module used
         and push it into the cache
        """

        obj_dict = {'connection': connection}

        self._cache.register(obj_dict, alias=alias)

    def _get_cache(self, alias=None):
        """
         Overlay _cache.switch using dictionary
         Get from cache the dictionary contain dbconnection and api_module
         and return them
        """
        obj_dict = self._cache.switch(alias)
        db_connection = obj_dict['connection']

        return db_connection

    def connect_to_mongodb(self, dbHost='localhost', dbPort=27017, dbMaxPoolSize=10, dbNetworkTimeout=None,
                           dbDocClass=dict, dbTZAware=False, uri=None, alias=None):
        """
        Loads pymongo and connects to the MongoDB host using parameters submitted.

        Example usage:
        | # To connect to foo.bar.org's MongoDB service on port 27017 |
        | Connect To MongoDB | foo.bar.org | ${27017} |
        | # Or for an authenticated connection, note addtion of "mongodb://" to host uri |
        | Connect To MongoDB | mongodb://admin:admin@foo.bar.org | ${27017} |
        | # Or for an connection with db uri |
        | Connect To MongoDB | mongodb://admin:admin@foo.bar.org/27017 |

        Added new field alias
        """

        dbPort = int(dbPort)
        print("| Connect To MongoDB | dbHost | dbPort | dbMaxPoolSize | dbNetworktimeout | dbDocClass | dbTZAware |")
        print("| Connect To MongoDB | %s | %s | %s | %s | %s | %s |" % (dbHost, dbPort, dbMaxPoolSize, dbNetworkTimeout,
                                                                        dbDocClass, dbTZAware))
        if uri:
            db_connection = MongoClient(host=uri)
        else:
            db_connection = MongoClient(host=dbHost, port=dbPort, socketTimeoutMS=dbNetworkTimeout,
                                        document_class=dbDocClass, tz_aware=dbTZAware,
                                        maxPoolSize=dbMaxPoolSize)

        self._push_cache(alias, db_connection)

    def disconnect_from_mongodb(self, alias=None):
        """
        Disconnects from the MongoDB server.

        For example:
        | Disconnect From MongoDB | # disconnects from current connection to the MongoDB server |

        Added new field alias
        """
        print("| Disconnect From MongoDB |")

        connection = self._get_cache(alias)
        connection.close()
