# -*- coding: utf-8 -*-

from mysql.connector import connect, Error
from connect.config import host, user, password, database


class DataBase():
    _instance = None
    cnx = None
    host = None
    user = None
    password = None
    database = None

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(DataBase, self).__new__(self)
            self.connect(self)
        return self.instance

    def connect(self):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

        self.cnx = connect(
            host=self.host, user=self.user,
            password=self.password, database=self.database)

    def query(self, query):
        try:
            cursor = self.cnx.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            return e

    def query_insert(self, query, params=None):
        try:
            cursor = self.cnx.cursor()
            cursor.execute(query, params)
            self.cnx.commit()
            cursor.close()
        except Error as e:
            print(e)

    def disconnect(self):
        self.cnx.close()

    def __del__(self):
        try:
            self.disconnect()

        except ImportError:
            print('Что-то пошло не так')

    def insert_log(self, last_query):
        self.connect()
        query = f'''INSERT INTO logs_table (date_time, last_query)
        VALUES (CURRENT_TIMESTAMP, '{last_query}');'''
        self.query_insert(query)
