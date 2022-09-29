import sqlite3
import credentials
import logger


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
        #
        # query = "CREATE TABLE IF NOT EXISTS properties (" \
        #         "   prop_id INTEGER PRIMARY KEY AUTOINCREMENT," \
        #         "   user_id INTEGER NOT NULL," \
        #         "   loc_id INTEGER NOT NULL," \
        #         "   price INTEGER NOT NULL," \
        #         "   avail_id INTEGER NOT NULL," \
        #         "   area INTEGER NOT NULL," \
        #         "   FOREIGN KEY (avail_id) REFERENCES avail(avail_id)," \
        #         "   FOREIGN KEY (loc_id) REFERENCES locations(loc_id)" \
        #         ");"
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

    def ex(self, query: str, commit=False, close=True, trans=False, fetch=True) -> list | None:
        """
        Executes *validated* SQL queries
        :param fetch: Should the results be returned
        :param trans: Should the query run as part of a transaction (DEPRECATED)
        :param close: Close the connection when done. Use with care
        :param query: The *validated* query to be executed
        :param commit: Commit the query
        :return: The reply of the query (if any)
        """
        logger.log(f'SQL: Executing: {query}')

        self.conn = sqlite3.connect(self.db, check_same_thread=False)
        self.cur = self.conn.cursor()
        results = []

        if trans:
            self.cur.execute('BEGIN TRANSACTION')
            commit = True

        try:
            self.cur.execute(query)

            if commit:
                self.conn.commit()
        except sqlite3.Error as err:
            if trans:
                pass
            logger.log(f'SQL: Error Response: {err}', level='ERROR')
            return None

        if fetch:
            results = self.cur.fetchall()
        if close:
            self.close()

        return [*results]

    def close(self) -> None:
        # Implicitly close cursor and connection

        self.cur.close()
        self.conn.close()


conn = Connector(db=credentials.database)


if __name__ == '__main__':
    conn = Connector(db=credentials.database)
    assert conn.ex('SELECT * FROM avail;', close=False, fetch=True) == [(1, 'Ενοικίαση'), (2, 'Πώληση')]
    assert conn.ex('SELECT * FROM locations;', close=True, fetch=True) == [(1, 'Αθήνα'), (2, 'Θεσσαλονίκη'), (3, 'Πάτρα'), (4, 'Ηράκλειο')]

