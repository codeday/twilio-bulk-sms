from os import getenv

from sqlalchemy import *
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship

postgres_db = {
    "drivername": "postgres",
    "username": getenv("DB_USERNAME", "postgres"),
    "password": getenv("DB_PASSWORD"),
    "database": getenv("DB_DB", "twilio-bulk-sms"),
    "host": getenv("DB_HOST", "10.0.3.34"),
    "port": 5432,
}
postgres_url = URL(**postgres_db)
engine = create_engine(postgres_url)
metadata = MetaData()

Base = declarative_base(bind=engine, metadata=metadata)


class Group(Base):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True)
    group_name = Column(String, nullable=False, unique=True)
    numbers = relationship("Number", back_populates="group", cascade="all, delete")

    def to_dict(self):
        return {
            'name':self.group_name,
            'id': self.id,
            'numbers':[str(number) for number in self.numbers]
        }


class Number(Base):
    __tablename__ = "number"
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("group.id"))
    number = Column(String, unique=True, nullable=False)
    group = relationship("Group", back_populates="numbers", cascade="all, delete")

    def __str__(self):
        return str(self.number)

def session_creator() -> Session:
    session = sessionmaker(bind=engine)
    return session()


global_session: Session = session_creator()
