import db_con
import logger
import bcrypt
import credentials
import re

types = ('location', 'availability', 'pwd', 'area', 'price')
valid = {}

sql_query = "SELECT location FROM locations;"
valid['location'] = [loc[0] for loc in db_con.conn.ex(sql_query, close=False)]
logger.log(f"Valid locations set to {valid['location']}")

sql_query = "SELECT availability FROM avail"
valid['availability'] = [avail[0] for avail in db_con.conn.ex(sql_query, close=False)]
logger.log(f"Availabilities set to {valid['availability']}")


def validate(text, dtype: str) -> bool:

    if dtype not in types:
        logger.log(f'{dtype} not valid', level='ERROR')
        return False

    if dtype == types[2]:
        pass

    if dtype in types[3:]:
        if is_int(text):
            if dtype == types[3]:
                return 20 <= int(text) <= 1000
            if dtype == types[4]:
                return 50 <= int(text) <= 5000000
        return False
    try:
        return text in valid[dtype]
    except KeyError:
        return False


def is_int(text) -> bool:
    if isinstance(text, int):
        return True
    try:
        int(text)
        return True
    except ValueError:
        pass
    return False


def is_email(text) -> bool:
    # Check if text is of example@example-domain.com format
    return bool(re.match(r'^[a-z0-9._-]+@[a-z0-9._-]+.[a-z]+$', text))


def pwd_check(pwd: str) -> bool:
    """
    Checks if the given pwd satisfies the criteria:
    - At least 8 characters long, less than or equal 30
    - At least one digit 0-9
    - At least one uppercase and one lowercase character
    :param pwd: str
    :return: bool
    """

    cases = []

    # Longer than or equal to 8 characters and shorter or equal to 30
    cases.append(8 <= len(pwd) <= 30)

    # At least one digit
    cases.append([char for char in pwd if char.isnumeric()])

    # Upper & lower character
    cases.append([x for x in pwd if x.islower()] != [] and [x for x in pwd if x.isupper()])

    return all(cases)  # TODO: make it so it returns a tuple with which condition failed if it did.


def enc_pwd(pwd: str) -> bytes:
    # Password hashing with salt

    logger.log(f'Password encryption', level='DEBUG')
    return bcrypt.hashpw(pwd.encode(), credentials.salt)

if __name__ == '__main__':
    for loc in ('Αθήνα', 'Θεσσαλονίκη', 'Πάτρα', 'Ηράκλειο'):
        assert validate(loc, 'location')
    assert not validate('Αθηνα', 'location')

    for avail in ('ενοικίαση','πώληση'):
        assert validate(avail, 'availability')
    assert not validate('ενoικίαση', 'availability')  # Character 'o' is English

    assert is_int(10)
    assert is_int('10')
    assert not is_int('text')
    assert validate(20, 'area')
    assert validate('20', 'area')
    assert not validate(19, 'area')
    assert not validate(1001, 'area')
    assert validate(50, 'price')
    assert not validate(49, 'price')
    assert not validate(5000001, 'price')
    assert enc_pwd('Anath3ma') == b'$2b$12$yjghy7zSpIF.sQQJ7wUKfu3M7vpGSlIyg7G/CdAU7jZdq.gHFkWSO'