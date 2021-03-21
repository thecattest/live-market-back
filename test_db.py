from db_init import *
from parse_items_xml import get_sample_json


db = db_session.create_session()


def test_data():
    thecattest = User()
    thecattest.login = "thecattest"
    thecattest.set_password("qwerty")
    thecattest.twitch_nickname = "the_cattest"
    db.add(thecattest)
    db.commit()
    return thecattest


def load_test_data():
    thecattest = db.query(User).first()
    return thecattest


thecattest = test_data()

print(thecattest)
