import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
level = 'DEBUG'


def dec(*args, **kwargs):
    # Basic wrapper for logging

    def wrapper(func):
        if kwargs['level'] == 'DEBUG':
            logging.debug(func)
        elif kwargs['level'] == 'INFO':
            logging.info(func)
        elif kwargs['level'] == 'WARN':
            logging.warning(func)
        return func

    return wrapper


def log(*args: str, **kwargs: str) -> None:
    # Basic logger

    if not kwargs:
        logging.debug(*args)
    elif kwargs['level'] == 'INFO':
        logging.info(*args)
    elif kwargs['level'] == 'WARN':
        logging.warning(*args)
    elif kwargs['level'] == 'ERROR':
        logging.error(*args)


if __name__ == '__main__':
    pass