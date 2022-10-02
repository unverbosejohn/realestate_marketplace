import sqlite3
import credentials
import logger
import time


class Connector:
    def __init__(self, db):
        self.db = db
        self.conn = None
        self.cur = None

        # ** Database schema start **
        #
        # query = "PRAGMA foreign_keys = ON;"
        # self.ex(query, commit=True, close=False)

        # query = "CREATE TABLE IF NOT EXISTS locations (" \
        #         "   loc_id INTEGER PRIMARY KEY," \
        #         "   location varchar(30) NOT NULL" \
        #         ");"
        # self.ex(query, commit=True, close=False)
        #
        # query = "CREATE TABLE IF NOT EXISTS avail (" \
        #         "   avail_id INTEGER PRIMARY KEY," \
        #         "   availability varchar(20) NOT NULL" \
        #         ");"
        # self.ex(query, commit=True, close=False)

        # query = "CREATE TABLE IF NOT EXISTS users (" \
        #         "  user_id int NOT NULL" \
        #         "  first_name varchar(45) NOT NULL," \
        #         "  last_name varchar(45) NOT NULL," \
        #         "  email varchar(45) NOT NULL," \
        #         "  password varchar(64) NOT NULL," \
        #         "  created_on DATETIME DEFAULT CURRENT_TIMESTAMP," \
        #         "  PRIMARY KEY (user_id)" \
        #         ");"
        # self.ex(query, commit=True)
        # New user query:
        # INSERT INTO users (username, first_name, last_name, email, password) VALUES("Doe", "Nick", "Doe", "nick.doe@gmail.com", "b'$2b$12$yjghy7zSpIF.sQQJ7wUKfuVvCZw99GJZTnv8ht2GmIV5FmTwvXAR.'");

        # CREATE TABLE IF NOT EXISTS properties (   prop_id INTEGER PRIMARY KEY,   user_id INTEGER NOT NULL,   loc_id INTEGER NOT NULL,   price INTEGER NOT NULL,   avail_id INTEGER NOT NULL,   area INTEGER NOT NULL,   FOREIGN KEY (avail_id) REFERENCES avail(avail_id),   FOREIGN KEY (loc_id) REFERENCES locations(loc_id), FOREIGN KEY (user_id) REFERENCES users(user_id));
        # INSERT INTO "main"."properties" ("prop_id", "user_id", "loc_id", "price", "avail_id", "area") VALUES ('5', '2', '2', '55000', '2', '120');
        # INSERT INTO "main"."properties" ("prop_id", "user_id", "loc_id", "price", "avail_id", "area") VALUES ('41', '1', '1', '200', '1', '55');
        # INSERT INTO "main"."properties" ("prop_id", "user_id", "loc_id", "price", "avail_id", "area") VALUES ('44', '1', '1', '550', '1', '650');
        # INSERT INTO "main"."properties" ("prop_id", "user_id", "loc_id", "price", "avail_id", "area") VALUES ('46', '1', '2', '1500', '1', '35');
        # INSERT INTO "main"."properties" ("prop_id", "user_id", "loc_id", "price", "avail_id", "area") VALUES ('48', '1', '1', '500', '1', '600');
        # INSERT INTO "main"."properties" ("prop_id", "user_id", "loc_id", "price", "avail_id", "area") VALUES ('49', '1', '1', '200', '1', '65');
        # INSERT INTO "main"."properties" ("prop_id", "user_id", "loc_id", "price", "avail_id", "area") VALUES ('52', '1', '1', '600', '1', '50');
        # INSERT INTO "main"."properties" ("prop_id", "user_id", "loc_id", "price", "avail_id", "area") VALUES ('53', '2', '1', '5000000', '2', '1000');
        # INSERT INTO "main"."properties" ("prop_id", "user_id", "loc_id", "price", "avail_id", "area") VALUES ('55', '1', '1', '65000', '2', '100');
        # INSERT INTO "main"."properties" ("prop_id", "user_id", "loc_id", "price", "avail_id", "area") VALUES ('56', '1', '4', '300', '1', '65');

        # query = "CREATE TABLE IF NOT EXISTS properties (" \
        #         "   prop_id INTEGER PRIMARY KEY," \
        #         "   user_id INTEGER NOT NULL," \
        #         "   loc_id INTEGER NOT NULL," \
        #         "   price INTEGER NOT NULL," \
        #         "   avail_id INTEGER NOT NULL," \
        #         "   area INTEGER NOT NULL," \
        #         "   FOREIGN KEY (user_id) REFERENCES users(user_id)," \
        #         "   FOREIGN KEY (avail_id) REFERENCES avail(avail_id)," \
        #         "   FOREIGN KEY (loc_id) REFERENCES locations(loc_id)" \
        #         ");"
        # print(query)
        # self.ex(query, commit=True)

        # query = f"INSERT INTO locations (loc_id, location) " \
        #         f"  VALUES" \
        #         f"      (1, 'Αθήνα')," \
        #         f"      (2, 'Θεσσαλονίκη')," \
        #         f"      (3, 'Πάτρα')," \
        #         f"      (4, 'Ηράκλειο');"
        # self.ex(query, commit=True, close=False)

        # query = f"INSERT INTO avail (avail_id, availability) " \
        #         f"  VALUES" \
        #         f"      (1, 'Ενοικίαση')," \
        #         f"      (2, 'Πώληση');"
        # self.ex(query, commit=True, close=True)

        #
        # ** Database schema end **

    def ex(self, query: str, data=None, fetch=True, commit=False):
        """
        Executes *validated* SQL queries
        :param query: str: SQL query, qmark format
        :param data: tuple: if qmark format is used, defaults None
        :param fetch: bool: Fetch results
        :param commit: bool Commit after execution
        :return: Results of query
        """

        logger.log(f'SQL: Executing: {query} {data if data else ""}')

        self.conn = sqlite3.connect(self.db, check_same_thread=False)

        pragma_query = "PRAGMA foreign_keys = ON;"
        self.conn.execute(pragma_query)

        try:
            res = self.conn.execute(query, data) if data else self.conn.execute(query)
            if commit : self.conn.execute("COMMIT;")

        except sqlite3.Error as err:
            logger.log(f'SQL: Error Response: {err}', level='ERROR')
            return None

        return [*res]


    def close(self) -> None:
        # Implicitly close cursor and connection Deprecated. TODO: delete if not used

        self.conn.close()


conn = Connector(db=credentials.database)
# conn = Connector(db='main/db/rem_auth.db')

if __name__ == '__main__':
    conn = Connector(db='main/db/rem_auth.db')
    assert conn.ex('SELECT * FROM avail;', fetch=True) == [(1, 'Ενοικίαση'), (2, 'Πώληση')]
    assert conn.ex('SELECT * FROM locations;', fetch=True) == [(1, 'Αθήνα'), (2, 'Θεσσαλονίκη'), (3, 'Πάτρα'), (4, 'Ηράκλειο')]

