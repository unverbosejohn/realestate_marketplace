import logger
import db_con
import data


class User:
    def __init__(self, email: str, pwd: str):
        self.email = email
        self.pwd = pwd
        self.first_name = None
        self.last_name = None
        self.table = 'users'
        self.logged_in = False
        at_index = self.email.index('@')
        self.safe_email = self.email[0:3] + ("*" * len(self.email[3:at_index])) + self.email[at_index:]

    @logger.dec(level='INFO')
    def login(self) -> bool:
        # Authenticates the user with the provided credentials

        sql_query = f'SELECT * FROM {self.table} WHERE email="{self.email}" AND password="{data.enc_pwd(self.pwd)}";'
        results = db_con.conn.ex(sql_query)
        logger.log(f'Login attempt: {self.safe_email}')

        # Assert if the credentials are correct
        if results:
            logger.log(f'Login Successful {results}')
            self.first_name, self.last_name = results[0][1:3]
            self.logged_in = True
            return True

        logger.log(f'Login unsuccessful', level='DEBUG')  # TODO: add # of tries
        return False

    @logger.dec(level='DEBUG')
    def logout(self) -> bool:
        # Logs out the current user

        logger.log(f'Logging out: {self.safe_email}', level='DEBUG')
        self.email = None
        self.pwd = None
        self.first_name = None
        self.last_name = None
        self.logged_in = False
        self.safe_email = None
        return True  # TODO: unset variable that stores the class, or make cleanup function

    @logger.dec(level='INFO')
    def register(self) -> tuple[bool, str]:
        # Registers a user

        # Check that all values were entered
        if self.email and self.pwd and self.first_name and self.last_name:

            # Check if the provided email is valid
            if not data.is_email(self.email):
                return False, 'email'

            # Check if user already exists in the db
            sql_query = f'SELECT email from {self.table} WHERE email="{self.email}"'
            if db_con.conn.ex(sql_query):
                logger.log('Registration failed, user exists', level='DEBUG')
                return False, 'user'

            # Check if the password satisfies the criteria
            if not data.pwd_check(self.pwd):
                return False, 'pwd'

            # Create user account with provided credentials
            sql_query = f'INSERT INTO {self.table} (first_name, last_name, email, password) VALUES ("{self.first_name}",' \
                        f'"{self.last_name}", "{self.email}", "{data.enc_pwd(self.pwd)}");'
            db_con.conn.ex(sql_query, commit=True)

            logger.log(f'New user registration: {self.safe_email}')
            return True, ''

        return False, 'fields'


if __name__ == '__main__':
    pass