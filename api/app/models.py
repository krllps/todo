from .db import Base

import sqlalchemy as sqla
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"
    __mapper_args__ = {
        "eager_defaults": True,  # required in order to access columns with server defaults
    }

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(64), nullable=False, unique=True, index=True)
    email = sqla.Column(sqla.String(128), nullable=True, default=None, unique=True, index=True)
    telegram = sqla.Column(sqla.String(64), nullable=True, default=None, unique=True, index=True)
    password = sqla.Column(sqla.String(128), nullable=False)
    registered_on = sqla.Column(sqla.TIMESTAMP, nullable=True, server_default=sqla.func.now())
    date_of_birth = sqla.Column(sqla.Date, nullable=True, default=None)

    tasks = sqla.orm.relationship("Task", backref="user")

    def __repr__(self):
        return f"User. id: {self.id}, name: {self.name}, email: {self.email}, telegram: {self.telegram}, " \
               f"registered_on: {self.registered_on}, date_of_birth: {self.date_of_birth}"


class Task(Base):
    __tablename__ = "task"
    __mapper_args__ = {
        "eager_defaults": True
    }

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(128), nullable=False, index=True)
    description = sqla.Column(sqla.String(512), nullable=True, default=None)
    created_on = sqla.Column(sqla.TIMESTAMP, nullable=True, server_default=sqla.func.now())
    due = sqla.Column(sqla.TIMESTAMP, nullable=False, index=True)
    is_checked = sqla.Column(sqla.Boolean, nullable=False, default=False, index=True)

    user_id = sqla.Column(sqla.Integer, sqla.ForeignKey("user.id", ondelete="CASCADE"))
    reminder_type_id = sqla.Column(sqla.Integer, sqla.ForeignKey("reminder_type.id", ondelete="CASCADE"))

    def __repr__(self):
        return f"Task. id: {self.id}, user_id: {self.user_id}, name: {self.name}, due: {self.due}," \
               f" is_checked: {self.is_checked}"


class ReminderType(Base):
    __tablename__ = "reminder_type"

    id = sqla.Column(sqla.Integer, primary_key=True)
    type = sqla.Column(sqla.String(32), nullable=False, unique=True, index=True)

    tasks = sqla.orm.relationship("Task", backref="reminder_type")

    def __repr__(self):
        return f"ReminderType. id: {self.id}, type: {self.type}"
