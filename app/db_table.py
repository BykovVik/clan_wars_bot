from sqlalchemy import Table, Column, MetaData, Integer, String, ForeignKey, BigInteger, Boolean
from sqlalchemy.orm import mapper
from app.config import db_engine

metadata = MetaData()

clan = Table("clans", metadata,
    Column("id", Integer(), primary_key=True),
    Column("chat_name", String(256)),
    Column("chat_id", BigInteger()),
    Column("chat_item", Integer()),
    Column("chat_active", Boolean()),
)


user = Table("users", metadata,
    Column("id", Integer(), primary_key=True),
    Column("user_activation", Boolean()),
    Column("username", String(256)),
    Column("user_id", BigInteger()),
    Column("user_item", Integer()),
    Column("captcha_active", Boolean()),
    Column("captcha_error", Integer()),
    Column("users_clan", ForeignKey("clans.id", ondelete='CASCADE'))
)


metadata.create_all(db_engine)




