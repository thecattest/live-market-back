import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin

from .utils import lorem_ipsum


class Product(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    sku = sqlalchemy.Column(sqlalchemy.String(20), unique=False, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String(200), unique=False, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String(1000), nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=False)
    img_src = sqlalchemy.Column(sqlalchemy.String(300), nullable=True)
    # sku is a product id for https://hackathon.oggettoweb.com/checkout/cart/addmultiple/products/{sku1,sku2,sku3}

    stream_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("streams.id"))
    stream = orm.relation("Stream")

    def load_info_from_market(self):
        lorem_ipsum(self)

    def __repr__(self):
        return f"<Product {self.sku} {self.title} '{self.stream.title}'>"
