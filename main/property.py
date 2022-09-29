import logger
import db_con


class Property:
    """
    Basic property object, stores property data

    *Class functions*
    check_data: checks that the object variables satisfy certain criteria
    save: Inserts property data in the db
    delete_property: Deleted property data from the db
    listify: Returns human-readable details about the property, in a list
    """

    def __init__(self, user_id, prop_id=0, loc_id=0, price=0, avail_id=0, area=0, stored=False):
        self.loc_id = int(loc_id)
        self.prop_id = int(prop_id)
        self.price = int(price)
        self.avail_id = int(avail_id)
        self.area = int(area)
        self.user_id = int(user_id)
        self.stored = stored

    def check_data(self) -> list[bool]:
        # checks that the object variables satisfy certain criteria

        cases = []

        try:
            cases.append(50 <= int(self.price) <= 5000000)
            cases.append(int(self.loc_id) in loc_ids.keys())
            cases.append(int(self.avail_id) in avail_ids.keys())
            cases.append(20 <= int(self.area) <= 1000)

        except ValueError:
            return cases + [False]

        return cases

    def save(self) -> tuple:
        # Saves properties in the db, returns [bool, prop_id]

        self_check = self.check_data()

        if not all(self_check):
            logger.log(f'Property Data incorrect')
            return False, [i for i, x in enumerate(self_check) if not x][0]

        elif self.user_id and not self.stored:
            sql_query = f'INSERT INTO properties (' \
                        f'  user_id, loc_id, price, avail_id, area)' \
                        f'  VALUES(' \
                        f'      {self.user_id},' \
                        f'      {self.loc_id},' \
                        f'      {self.price},' \
                        f'      {self.avail_id},' \
                        f'      {self.area});'

            db_con.conn.ex(sql_query, trans=True, fetch=False, close=False)
            sql_query = 'SELECT seq FROM sqlite_sequence WHERE name="properties";'

            self.prop_id = int(db_con.conn.ex(sql_query, fetch=True, close=True)[0][0])

            logger.log(f'Property with id {self.prop_id} saved. {self}')
            self.stored = True

        return True, self.prop_id if self.prop_id else False, None

    def delete_property(self) -> bool:
        # Delete property from the database. Does not deconstruct class

        if self.stored:
            sql_query = f'DELETE FROM properties WHERE prop_id = {self.prop_id};'
            db_con.conn.ex(sql_query, trans=True, fetch=False, close=True)
            return True

        return False

    def listify(self) -> list[str]:
        # Returns the details of the property in a list, as strings, in human-readable format

        return [str(loc_ids[self.loc_id]), str(avail_ids[self.avail_id]), str(self.price) + ' ευρώ', str(self.area) + ' τ.μ.']


# Location: Location_id dictionary (cities)
locations = {location: loc_id for loc_id, location in [x for x in db_con.conn.ex('SELECT * FROM locations', close=False)]}

# Location_id: Location dictionary (cities)
loc_ids = {loc_id: location for location, loc_id in locations.items()}

# Availability: Availability_id dictionary
availability = {avail: avail_id for avail_id, avail in [x for x in db_con.conn.ex('SELECT * FROM avail')]}

# Availability_id: Availability dictionary
avail_ids = {avail_id: avail for avail, avail_id in availability.items()}


if __name__ == '__main__':
    pass
