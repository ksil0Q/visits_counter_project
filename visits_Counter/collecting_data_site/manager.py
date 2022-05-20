from models import User, Client
from pony.orm import *
from multipledispatch import dispatch
from werkzeug.security import check_password_hash


class UserManager(object):
    @db_session
    def add_visits(self, data: dict):
        User(
            cookies_uuid=data['cookie'],
            ip=data['ip'],
            time=data['time'],
            connection_date=data['date'],
            country=data['country'],
            region=data['region'],
            city=data['city'],
            zip=data['zip'],
            latitude=data['lat'],
            longitude=data['lon'],
            first_page=data['first_page']
        )
        return User


class ClientManager(object):
    @db_session
    def add_client(self, data: dict):
        Client(
            login=data['login'],
            email=data['email'],
            password_hash=data['password_hash'],
            cookies_uuid=data['cookies_uuid']
        )
        return Client

    @dispatch(str)
    @db_session
    def is_registered(self, cookie_uuid: str) -> bool:
        if cookie_uuid:
            return False
        return Client.exists(cookies_uuid=cookie_uuid)

    @dispatch(str, str)
    @db_session
    def is_registered(self, login: str, psw: str) -> bool:
        password = select(client.password_hash for client in Client.select()
                          if client.login == login or
                          client.email == login).first()
        if password:
            return check_password_hash(password, psw)
        return False

    @db_session
    def number_of_logged_in_clients(self):
        return count(client for client in Client.select())
