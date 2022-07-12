from .db import Base

import sqlalchemy as sqla
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"
    __mapper_args__ = {"eager_defaults": True}  # required in order to access columns with server defaults

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(50), nullable=False, unique=True, index=True)
    email = sqla.Column(sqla.String(100), nullable=True, default=None, unique=True, index=True)
    password = sqla.Column(sqla.String(100), nullable=False)
    registered_on = sqla.Column(sqla.DateTime, nullable=False, server_default=sqla.func.now())
    data_of_birth = sqla.Column(sqla.Date, nullable=True, default=None)

    tasks = relationship("Task", backref="user")

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, email: {self.email}"


class Task(Base):
    __tablename__ = "task"
    __mapper_args__ = {"eager_defaults": True}  # required in order to access columns with server defaults

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(100), nullable=False, index=True)
    description = sqla.Column(sqla.String(300), nullable=True, default=None)
    created_on = sqla.Column(sqla.DateTime, nullable=True, server_default=sqla.func.now())
    due = sqla.Column(sqla.DateTime, nullable=False, index=True)
    is_checked = sqla.Column(sqla.Boolean, nullable=False, default=False, index=True)

    user_id = sqla.Column(sqla.Integer, sqla.ForeignKey("user.id"))

    def __repr__(self):
        return f"id: {self.id}, user_id: {self.user_id}, name: {self.name}, due: {self.due}," \
               f" is_checked: {self.is_checked}"
