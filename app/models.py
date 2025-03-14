from tkinter.constants import CASCADE

from .database import Base
from sqlalchemy import Integer, String, Column, TIMESTAMP, text, ForeignKey


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    username = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Tasks(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False)
    priority = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey('users.id', ondelete=CASCADE),nullable=False)