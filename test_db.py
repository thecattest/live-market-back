from db_init import *


db = db_session.create_session()


def test_data():
    thecattest = User()
    thecattest.login = "thecattest"
    thecattest.set_password("thecattestpasswordisqwerty")

    stream = Stream()
    stream.title = "Test Stream"
    stream.owner = thecattest

    product = Product()
    product.sku = "24-MB01"
    product.load_info_from_market()
    stream.products.append(product)

    db.add(thecattest)
    db.add(stream)
    db.add(product)
    db.commit()

    return thecattest, stream, product


def load_test_data():
    thecattest = db.query(User).first()
    stream = db.query(Stream).first()
    product = db.query(Product).first()
    return thecattest, stream, product


thecattest, stream, product = load_test_data()

print(product.to_dict(only=("id", "sku", "title", "description", "price", "img_src", "stream_id")))
print(product)
print()
print(stream.to_dict(only=("id", "title")))
print(stream)
print()
print(thecattest)
