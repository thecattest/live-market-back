import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_file, ip=None, username=None, password=None):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Specify db file")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    # conn_str = f'mysql+pymysql://{username}:{password}@{ip}/{db_file}?charset=utf8'
    # print(f"Connecting {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
