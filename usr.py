import logger
import db_con
import property
import time

class User:
    def __init__(self, user_id: int, username: str, pwd: str):
        self.user_id = user_id
        self.username = username
        self.password = pwd
        self.logged_in = False
        self.properties = {}

    def __enter__(self):
        return self

    def __repr__(self):
        return f'User connected: {self.username}'

    def get_properties(self):

        # Gets the user's properties from the db. Saved in self.properties (dict)
        query = f'SELECT prop_id, loc_id, price, avail_id, area' \
                f'  FROM properties' \
                f'  WHERE user_id = "{self.user_id}";'
        results = db_con.conn.ex(query, close=True)

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

    def del_property(self, prop_id: int) -> bool:
        # Deletes a property from self.properties dict and calls for deletion from db

        self.properties[prop_id].delete_property()
        del self.properties[prop_id]

        while prop_id in self.properties.keys():
            time.sleep(0.2)

        return True


users = []
users.append(User(user_id=1, username='john', pwd='password'))
users.append(User(user_id=2, username='doe', pwd='secret'))
logger.log(f'You can connect to the frontend using login: john, pass: password')


if __name__ == '__main__':
    pass