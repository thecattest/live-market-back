from db_init import *
from parse_items_xml import get_sample_json


db = db_session.create_session()


def test_data():
    thecattest = User()
    thecattest.login = "thecattest"
    thecattest.set_password("qwerty")

    stream = Stream()
    stream.title = "Test Stream"
    stream.owner = thecattest
    products_json = get_sample_json()
    stream.products = products_json

    db.add(thecattest)
    db.add(stream)
    db.commit()

    return thecattest, stream


def load_test_data():
    thecattest = db.query(User).first()
    stream = db.query(Stream).first()
    return thecattest, stream


thecattest, stream = test_data()

print(stream.to_dict(only=("id", "title")))
print(stream)
print()
print(thecattest)
print()
print(stream.products)
