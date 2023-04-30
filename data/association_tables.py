import sqlalchemy

from data.db_session import SqlAlchemyBase

association_table = sqlalchemy.Table(
    'account_to_course',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column("accounts", sqlalchemy.Integer, sqlalchemy.ForeignKey("accounts.id")),
    sqlalchemy.Column("courses", sqlalchemy.Integer, sqlalchemy.ForeignKey("courses.id"))
)
