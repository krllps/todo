from .db import Base

import sqlalchemy as sqla
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.orm import relationship, validates

from datetime import datetime


class User(Base):
    __tablename__ = "user"
    __mapper_args__ = {
        "eager_defaults": True,  # required in order to access columns with server defaults
    }
    __table_args__ = (
        CheckConstraint("password >= 8"),  # db level validator (isn't discovered by alembic --autogenerate)
    )

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(64), nullable=False, unique=True, index=True)
    email = sqla.Column(sqla.String(128), nullable=True, default=None, unique=True, index=True)
    telegram = sqla.Column(sqla.String(64), nullable=True, default=None, unique=True, index=True)
    password = sqla.Column(sqla.String(128), nullable=False)
    registered_on = sqla.Column(sqla.DateTime, nullable=False, server_default=sqla.func.now())
    date_of_birth = sqla.Column(sqla.Date, nullable=True, default=None)

    tasks = sqla.orm.relationship("Task", backref="user")

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, email: {self.email}, telegram: {self.telegram}, " \
               f"registered_on: {self.registered_on}, date_of_birth: {self.date_of_birth}"

    @validates("password")  # orm level validator
    def password_must_be_longer_than_eight_chars(self, key, value):
        if len(value) < 8:
            raise ValueError("password must be longer than eight characters")
        return value


class Task(Base):
    __tablename__ = "task"
    __mapper_args__ = {"eager_defaults": True}

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(128), nullable=False, index=True)
    description = sqla.Column(sqla.String(512), nullable=True, default=None)
    created_on = sqla.Column(sqla.DateTime, nullable=True, server_default=sqla.func.now())
    due = sqla.Column(sqla.DateTime, nullable=False, index=True)
    is_checked = sqla.Column(sqla.Boolean, nullable=False, default=False, index=True)

    user_id = sqla.Column(sqla.Integer, sqla.ForeignKey("user.id", ondelete="CASCADE"))
    reminder = sqla.orm.relationship("Reminder", back_populates="task", uselist=False)

    def __repr__(self):
        return f"id: {self.id}, user_id: {self.user_id}, name: {self.name}, due: {self.due}," \
               f" is_checked: {self.is_checked}"

    @validates("due")
    def due_date_must_not_be_in_the_past(self, key, value):
        if value < datetime.now():
            raise ValueError("due date must not be in the past")
        return value


class Reminder(Base):
    __tablename__ = "reminder"

    id = sqla.Column(sqla.Integer, primary_key=True)
    via_email = sqla.Column(sqla.Boolean, nullable=False, default=False)
    via_telegram = sqla.Column(sqla.Boolean, nullable=False, default=False)
    remind_on = sqla.Column(sqla.DateTime, nullable=False, index=True)

    task_id = sqla.Column(sqla.Integer, sqla.ForeignKey("task.id"))
    task = sqla.orm.relationship("Task", back_populates="reminder")
