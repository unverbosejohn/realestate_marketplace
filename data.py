import db_con
import logger


class Val:
    def __init__(self):
        self.types = ('location', 'availability', 'area', 'price')
        self.valid = {}

        sql_query = "SELECT location FROM locations;"
        self.valid['locations'] = db_con.conn.ex(sql_query, close=False)

        sql_query = "SELECT availability FROM avail"
        self.valid['availability'] = db_con.conn.ex(sql_query, close=False)

    def validate(self, text, dtype: str) -> bool:

        if dtype not in self.types:
            logger.log(f'{dtype} not valid', level='ERROR')
            return False

        if dtype in self.types[2:]:
            if self.is_int(text):
                if dtype == self.types[2]:
                    return 20 <= int(text) <= 1000
                if dtype == self.types[3]:
                    return 50 <= int(text) <= 5000000
            return False

        return text in self.valid[dtype]

    def is_int(self, text) -> bool:
        if isinstance(text, int):
            return True
        try:
            int(text)
            return True
        except TypeError:
            pass
        return False


if __name__ == '__main__':

    test = Val()

    for loc in ('Αθήνα', 'Θεσσαλονίκη', 'Πάτρα', 'Ηράκλειο'):
        assert test.validate(loc, 'location') == True
    assert test.validate('Αθηνα', 'location') == False

    for avail in ('ενοικίαση','πώληση'):
        assert test.validate(avail, 'availability') == True
    assert test.validate('ενoικίαση', 'availability') == False

    assert test.validate(20, 'area')
    assert test.validate('20', 'area')
    assert not test.validate(19, 'area')
    assert not test.validate(1001, 'area')
    assert test.validate(50, 'price')
    assert not test.validate(49, 'price')
    assert not test.validate(5000001, 'price')