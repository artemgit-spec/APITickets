from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
)
from sqlalchemy.orm import DeclarativeBase, sessionmaker

import uuid

engine = create_engine(
    "postgresql+psycopg2://ticket_db:ticket_db@localhost:5432/ticket_db", echo=True
)
session = sessionmaker(bind=engine)


async def session_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    mail_users = Column(String)
    is_admin = Column(String, default="user")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    text_ticket = Column(Text)
    creating_ticket = Column(DateTime)
    closing_ticket = Column(DateTime, default=None)
    identifier = Column(String, unique=True, default=lambda: str(uuid.uuid4()))
    is_active = Column(String, default="active")
    id_user = Column(Integer)
