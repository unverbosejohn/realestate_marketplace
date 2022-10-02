import bcrypt
import logger as logger
import credentials as credentials


def enc_pwd(pwd: str) -> bytes:
    # Password hashing with salt

    logger.log(f'Password encryption using {credentials.salt}', level='DEBUG')
    return bcrypt.hashpw(pwd.encode(), credentials.salt)


@logger.dec(level='DEBUG')
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

    return all(cases)  # TODO: make it, so it returns a tuple with which condition failed if it did.

if __name__ == '__main__':
    pass