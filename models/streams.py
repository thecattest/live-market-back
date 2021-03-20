import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Stream(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'streams'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String(200), unique=False, nullable=False)
    products = sqlalchemy.Column(sqlalchemy.JSON, unique=False, nullable=True)
    # implement streams realization - here may be column with youtube stream link
    # like this
    # youtube_link = sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=False)

    # user holding stream
    owner_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    owner = orm.relation("User")

    def dict(self):
        return self.to_dict(only=("id", "title", "products", "owner_id"))

    def __repr__(self):
        return f"<Stream {self.id} '{self.title}' {self.owner.login}>"
