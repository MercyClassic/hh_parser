from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = 'sqlite:///sqlite.db'

engine = create_engine(DATABASE_URL)
session_maker = sessionmaker(engine, class_=Session, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
