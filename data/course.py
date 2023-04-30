import sqlalchemy
from sqlalchemy import orm
import datetime
from .db_session import SqlAlchemyBase


class Course(SqlAlchemyBase):
    __tablename__ = 'courses'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    date_of_creation = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    topics = orm.relationship("Topic", back_populates='course')


class Topic(SqlAlchemyBase):
    __tablename__ = 'topics'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    date_of_creation = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    name = sqlalchemy.Column(sqlalchemy.String)
    content = sqlalchemy.Column(sqlalchemy.String)

    course_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("courses.id"))
    course = orm.relationship('Course', foreign_keys=[course_id], lazy=False)


