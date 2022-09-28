import db_con
import logger


types = ('location', 'availability', 'pwd', 'area', 'price')
valid = {}

sql_query = "SELECT * FROM locations;"
cities = {id: city for id, city in [loc for loc in db_con.conn.ex(sql_query, close=False)]}
logger.log(f"Valid locations set to {cities}")

sql_query = "SELECT * FROM avail"
availability = {id: avail for id, avail in [av for av in db_con.conn.ex(sql_query, close=False)]}
logger.log(f"Availabilities set to {availability}")


def is_int(text) -> bool:
    if isinstance(text, int):
        return True
    if not isinstance(text, float):
        try:
            int(text)
            return True
        except ValueError:
            pass
    return False


if __name__ == '__main__':
    assert is_int(10)
    assert not is_int(10.5)
    assert not is_int('10 τ.μ.')
    assert is_int('10')
    assert not is_int('text')
