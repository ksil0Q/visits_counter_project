from pony import orm
from datetime import date, time
from db_init import db


class User(db.Entity):
    _table_ = 'users'
    id = orm.PrimaryKey(int, auto=True)
    cookies_uuid = orm.Required(str)
    ip = orm.Required(str)
    time = orm.Optional(time)
    connection_date = orm.Required(date)
    country = orm.Required(str)
    region = orm.Required(str)
    city = orm.Required(str)
    zip = orm.Required(int)
    latitude = orm.Required(float)
    longitude = orm.Required(float)
    first_page = orm.Required(str)


class Client(db.Entity):
    _table_ = 'clients'
    id = orm.PrimaryKey(int, auto=True)
    email = orm.Required(str)
    login = orm.Required(str)
    password_hash = orm.Required(str)
    cookies_uuid = orm.Required(str)


db.generate_mapping(create_tables=True)
