import os
from dataclasses import dataclass, asdict
from sqlalchemy import create_engine, orm, text
from sqlalchemy.engine.url import URL
from dotenv import load_dotenv
load_dotenv()


@dataclass
class DBConfig:
    host: str = os.environ.get("host")
    port: int = int(os.environ.get("port"))
    user: str = os.environ.get("user")
    pw: str = os.environ.get("pw")
    db: str = os.environ.get("db")


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class DBConnector(metaclass=Singleton):
    def __init__(self, **kwargs):
        self.host = kwargs.get('host')
        self.port = kwargs.get('port')
        self.user = kwargs.get('user')
        self.pw = kwargs.get('pw')
        self.db = kwargs.get('db')
        self.engine = None
        self.session = None

    def create_session(self):
        if self.engine is None:
            url = URL.create(
                drivername='postgresql+psycopg2',
                username=self.user,
                password=self.pw,
                host=self.host,
                port=self.port,
                database=self.db
            )
            self.engine = create_engine(url, echo=False, connect_args={"channel_binding": "disable"})
            Session = orm.sessionmaker()
            Session.configure(bind=self.engine)
            self.session = Session()
        return self.session

dbConnector = DBConnector(**asdict(DBConfig()))
session = dbConnector.create_session()
session.execute(text("select 1"))
session.close()

