import logger
import db_con
import property
import time
import auth
import credentials
from datetime import datetime
import datetime


class User:
    """
    User object, stores user data

    *Class functions*
    get_properties: Fetches all user properties from the db
    del_property: Deletes a property for the user, calls property.delete_property

    """

    def __init__(self, username: str, pwd=None):
        self.user_id = None
        self.username = username
        self.first_name = None
        self.last_name = None
        self.email = None
        self.password = pwd
        self.logged_in = False
        self.properties = {}
        self.tries = 0
        self.last_try = None

    def __enter__(self):
        return self

    def __repr__(self):
        return f'User connected: {self.username}'

    def login(self) -> bool:
        # Authenticates the user with the provided credentials

        # Check for number of failed attempts and throttle.
        if self.tries > 3:
            if datetime.datetime.now() - self.last_try < datetime.timedelta(seconds=5):
                logger.log(f'Username {self.username} login attempt throttled.')
                return False

        sql_query = 'SELECT user_id, username, first_name, last_name, email FROM users WHERE username= %s AND password = %s'
        data = (self.username, auth.enc_pwd(self.password).decode())

        results = db_con.conn.ex(sql_query, data=data, fetch=True)
        logger.log(f'Login attempt using username {self.username}', level='INFO')

        # Assert if the credentials are correct and set user details
        if results:
            logger.log(f'Login Successful. Results: {results}', level='INFO')
            self.user_id = results[0][0]
            self.first_name, self.last_name, self.email = results[0][2:5]
            self.logged_in = True
            self.tries = 0
            self.last_try = None
            return True

        logger.log(f'Login unsuccessful', level='DEBUG')
        self.tries += 1
        self.last_try = datetime.datetime.now()
        return False

    def get_details(self):
        sql_query = 'SELECT user_id, username, first_name, last_name, email FROM users WHERE username= %s'
        data = (str(self.username),)
        results = db_con.conn.ex(sql_query, data=data, fetch=True)
        if results:
            self.user_id = results[0][0]
            self.first_name, self.last_name, self.email = results[0][2:5]
            self.logged_in = True
            self.tries = 0
            self.last_try = None
            return True
        return False

    def get_properties(self):

        # Gets the user's properties from the db. Saved in self.properties (dict)
        query = f'SELECT prop_id, loc_id, price, avail_id, area' \
                f'  FROM properties' \
                f'  WHERE user_id = %s'
        results = db_con.conn.ex(query, fetch=True, data=(self.user_id,))

        if not results:
            return False

        for result in results:
            self.properties[result[0]] = property.Property(
                prop_id=result[0],
                user_id=self.user_id,
                loc_id=result[1],
                price=result[2],
                avail_id=result[3],
                area=result[4],
                stored=True
            )
        return True

    def del_property(self, prop_id: int) -> bool:
        # Deletes a property from self.properties dict and calls for deletion from db

        self.properties[prop_id].delete_property()
        del self.properties[prop_id]

        while prop_id in self.properties.keys():
            time.sleep(0.2)

        return True


# User credentials are stored here
# username = 'john'
# password = 'password'

# users = [User(username='john', pwd='password'), User(username='doe', pwd='secret')]
# logger.log(f'You can connect to the frontend using login: john, pass: password')


if __name__ == '__main__':
    user01 = User(username='john', pwd='password')
    assert user01.login()

