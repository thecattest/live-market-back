import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin

from hashlib import md5
from werkzeug.security import check_password_hash, generate_password_hash


class User(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String(100), unique=True, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    twitch_nickname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    products = sqlalchemy.Column(sqlalchemy.JSON, unique=False, nullable=True)
    stream_started = sqlalchemy.Column(sqlalchemy.Boolean, default=False, nullable=False)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f"<User {self.id} {self.login}>"
