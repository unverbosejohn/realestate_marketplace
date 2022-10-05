import sqlite3
import credentials
import logger
import time
import os
import mysql.connector
from mysql.connector.constants import ClientFlag


class Connector:
    def __init__(self):
        self.config = credentials.db_config
        self.conn = None
        self.cur = None

        # ** Database schema start **
        #
        # query = "PRAGMA foreign_keys = ON;"
        # self.ex(query, commit=True, close=False)

        query = "USE rem_auth"
        self.ex(query, close=False)

        # query = "CREATE TABLE IF NOT EXISTS locations (" \
        #         "   loc_id INT AUTO_INCREMENT PRIMARY KEY," \
        #         "   location VARCHAR(30) NOT NULL" \
        #         ")"
        # self.ex(query, commit=True, close=False)
        #
        # query = "CREATE TABLE IF NOT EXISTS avail (" \
        #         "   avail_id INT AUTO_INCREMENT PRIMARY KEY," \
        #         "   availability VARCHAR(20) NOT NULL" \
        #         ")"
        # self.ex(query, commit=True, close=False)
        #
        # query = "CREATE TABLE IF NOT EXISTS users (" \
        #         "  user_id INT AUTO_INCREMENT PRIMARY KEY," \
        #         "  username VARCHAR(20) NOT NULL," \
        #         "  first_name VARCHAR(45) NOT NULL," \
        #         "  last_name VARCHAR(45) NOT NULL," \
        #         "  email VARCHAR(45) NOT NULL," \
        #         "  password VARCHAR(64) NOT NULL," \
        #         "  created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP" \
        #         ")"
        # self.ex(query, commit=True, close=False)
        #
        # # New user query:
        # # INSERT INTO users (username, first_name, last_name, email, password) VALUES("Doe", "Nick", "Doe", "nick.doe@gmail.com", "b'$2b$12$yjghy7zSpIF.sQQJ7wUKfuVvCZw99GJZTnv8ht2GmIV5FmTwvXAR.'");
        #
        # query = 'CREATE TABLE IF NOT EXISTS properties (' \
        #             '   prop_id INT AUTO_INCREMENT PRIMARY KEY,' \
        #             '   user_id INT NOT NULL,' \
        #             '   loc_id INT NOT NULL,' \
        #             '   price INT NOT NULL,' \
        #             '   avail_id INT NOT NULL,' \
        #             '   area INT NOT NULL,' \
        #             '   FOREIGN KEY (avail_id)' \
        #             '       REFERENCES avail(avail_id)' \
        #             '       ON UPDATE RESTRICT ON DELETE CASCADE,' \
        #             '   FOREIGN KEY (loc_id)' \
        #             '       REFERENCES locations(loc_id)' \
        #             '       ON UPDATE RESTRICT ON DELETE CASCADE,' \
        #             '   FOREIGN KEY (user_id)' \
        #             '       REFERENCES users(user_id)' \
        #             '       ON UPDATE RESTRICT ON DELETE CASCADE' \
        #             ')'
        # self.ex(query, commit=True, close=True)

        #
        # query = "INSERT INTO locations (loc_id, location) VALUES ( %s, %s)"
        # data = [
        #     (1, 'Αθήνα'),
        #     (2, 'Θεσσαλονίκη'),
        #     (3, 'Πάτρα'),
        #     (4, 'Ηράκλειο')
        #     ]
        #
        # self.ex(query, data=data, commit=True, close=False)
        #
        # query = "INSERT INTO avail (avail_id, availability) VALUES ( %s, %s )"
        # data = [
        #     (1, 'Ενοικίαση'),
        #     (2, 'Πώληση')
        #     ]
        # self.ex(query, data=data, commit=True, close=True)

        #
        # ** Database schema end **

    def ex(self, query: str, data=None, fetch=True, commit=False, close=True):
        """
        Executes *validated* SQL queries
        :param query: str: SQL query, qmark format
        :param data: tuple: if qmark format is used, defaults None
        :param fetch: bool: Fetch results
        :param commit: bool Commit after execution
        :return: Results of query
        """
        self.config = credentials.db_config

        logger.log(f'SQL: Executing: {query} {data if data else ""}')
        self.conn = mysql.connector.connect(**self.config)
        self.cur = self.conn.cursor()
        res = []

        try:
            if data:
                if isinstance(data, list):
                    self.cur.executemany(query, data)
                else:
                    self.cur.execute(query, data)
            else:
                self.cur.execute(query)
            if commit : self.cur.execute("COMMIT;")
            if fetch:
                res = self.cur.fetchall()

        except mysql.connector.Error as err:
            logger.log(f'SQL: Error Response: {err}', level='ERROR')
            if close : self.close()
            return None

        if close : self.close()
        logger.log(res)
        return [*res] if res else None

    def close(self) -> None:
        # Implicitly close cursor and connection
        self.cur.close()
        self.conn.close()

conn = Connector()
# conn = Connector(db='main/db/rem_auth.db')

if __name__ == '__main__':
    conn = Connector(config=credentials.db_config)
    assert conn.ex('SELECT * FROM avail;', fetch=True) == [(1, 'Ενοικίαση'), (2, 'Πώληση')]
    assert conn.ex('SELECT * FROM locations;', fetch=True) == [(1, 'Αθήνα'), (2, 'Θεσσαλονίκη'), (3, 'Πάτρα'), (4, 'Ηράκλειο')]

