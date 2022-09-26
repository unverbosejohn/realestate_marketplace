import sqlite3
import auth
import credentials
import logger


class Connector:
    def __init__(self, db):
        self.db = db
        self.conn = None
        self.cur = None

        query = "PRAGMA foreign_keys = ON;"
        self.ex(query, commit=True, close=False)

        query = "CREATE TABLE IF NOT EXISTS users (" \
                "   user_id INTEGER PRIMARY KEY NOT NULL UNIQUE," \
                "   first_name varchar(45) NOT NULL," \
                "   last_name varchar(45) NOT NULL," \
                "   email varchar(45) NOT NULL," \
                "   password varchar(64) NOT NULL," \
                "   created_on DATETIME" \
                ");"
        self.ex(query, commit=True, close=False)

        query = "CREATE TABLE IF NOT EXISTS locations (" \
                "   loc_ID INTEGER PRIMARY KEY," \
                "   location varchar(30) NOT NULL" \
                ");"
        self.ex(query, commit=True, close=False)

        query = "CREATE TABLE IF NOT EXISTS avail (" \
                "   avail_id INTEGER PRIMARY KEY," \
                "   availability varchar(20) NOT NULL" \
                ");"
        self.ex(query, commit=True, close=False)

        query = "CREATE TABLE IF NOT EXISTS properties (" \
                "   prop_id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "   user_id INTEGER NOT NULL," \
                "   loc_id INTEGER NOT NULL," \
                "   price INTEGER NOT NULL," \
                "   avail_id INTEGER NOT NULL," \
                "   area INTEGER NOT NULL," \
                "   FOREIGN KEY (avail_id) REFERENCES avail(avail_id)," \
                "   FOREIGN KEY (loc_ID) REFERENCES locations(loc_ID)," \
                "   FOREIGN KEY (user_id) REFERENCES users(user_id)" \
                ");"
        self.ex(query, commit=True)

    def ex(self, query: str, commit=False, close=True) -> list:
        """
        Executes *validated* SQL queries
        :param close: Close the connection when done. Use with care
        :param query: The *validated* query to be executed
        :param commit: Commit the query
        :return: The reply of the query (if any)
        """
        self.conn = sqlite3.connect(self.db)
        self.cur = self.conn.cursor()
        self.cur.execute(query)
        if commit:
            self.conn.commit()
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
