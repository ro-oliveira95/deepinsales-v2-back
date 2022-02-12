'''
Module to handle database queries
'''
from dis import findlinestarts
import os
import logging
from psycopg2 import pool
from decouple import config

logger = logging.getLogger(__name__)

DB_HOST = config('DB_HOST', '')
DB_USER = config('DB_USER', '')
DB_PASSOWRD = config('DB_PASSWORD', '')
DB_NAME = config('DB_NAME', '')
DB_PORT = config('DB_PORT', '')


class Database:
    '''
    Class to handle connection to database
    '''

    def __init__(self):
        self.user = DB_USER
        self.password = DB_PASSOWRD
        self.host = DB_HOST
        self.port = DB_PORT
        self.database = DB_NAME
        self._cursor = None

        self._connection_pool = None
        self.con = None

        self.connect()

    def connect(self):
        """
        Interface to create a connection pool
        """
        if not self._connection_pool:
            try:
                self._connection_pool = pool.ThreadedConnectionPool(
                    1,
                    20,
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port,
                    database=self.database,
                )
            except Exception as e:
                print(
                    'Some error occured while connecting to db'
                )
                raise e

    def fetch_one(self, query: str, data: tuple):
        '''
        Fetch one item from db
        '''
        try:
            self.con = self._connection_pool.getconn()
        except Exception as e:
            # raise Exception(
            #     'Error getting connection from db pool. \n {}'.format(e)
            # )
            raise e
        try:
            cur = self.con.cursor()
            print(query, data)
            cur.execute(query, data)
            self.con.commit()
        except Exception as e:
            self._connection_pool.putconn(self.con)
            # raise Exception('Error executing query.\n {}'.format(e))
            raise e
        try:
            result = cur.fetchone()[0]
            return result
        except Exception as e:
            raise Exception('Error fetching new id.\n {}'.format(e))
        finally:
            self._connection_pool.putconn(self.con)

    def fetch_many(self, query: str, data: tuple) -> list:
        '''
        Base to fetch multiple from db
        '''
        try:
            self.con = self._connection_pool.getconn()
        except Exception as e:
            raise Exception(
                'Error getting connection from db pool. \n {}'.format(e)
            )
        try:
            cur = self.con.cursor()
            print(query, data)
            cur.execute(query, data)
            column_names = [desc[0] for desc in cur.description]
        except Exception as e:
            self._connection_pool.putconn(self.con)
            raise Exception('Error executing query.\n {}'.format(e))

        try:
            rows = cur.fetchall()
            self._connection_pool.putconn(self.con)
        except Exception as e:
            self._connection_pool.putconn(self.con)
            raise Exception('Error fetching.\n {}'.format(e))

        try:
            # self._connection_pool.putconn(self.con)
            result = []
            if rows is not None:
                for row in rows:
                    result.append(dict(zip(column_names, row)))
                return result
        except Exception as e:
            self._connection_pool.putconn(self.con)
            raise Exception(
                'Error formatting databse return. \n {}'.format(e)
            )

db_instance = Database()