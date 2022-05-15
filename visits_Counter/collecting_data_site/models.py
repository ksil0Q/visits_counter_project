from pony import orm
from db_init import db
from dataclasses import dataclass
import re
from datetime import date
import requests
from http import cookies
import uuid
import datetime


class User(db.Entity):
    _table_ = 'users'
    id = orm.PrimaryKey(int, auto=True)
    cookies_uuid = orm.Required(str)
    ip = orm.Required(str)
    time = orm.Optional(datetime.time)
    connection_date = orm.Required(datetime.date)
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


@dataclass
class DataError:
    message: str = 'Successfully'
    validity: bool = True
    _password_pattern: str = r"^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=_]).*$"
    _email_pattern: str = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"

    def is_correct_data(self, login_name: str = None, email: str = None,
                        psw: str = None, psw2: str = None):
        if len(login_name) < 6 and login_name:
            self.message = 'Login must be longer than 5 characters'
            self.validity = False

        if not self.is_valid_email(email):
            self.message = 'Incorrect email address'
            self.validity = False

        if len(psw) < 6:
            self.message = 'Password must be longer than 5 characters'
            self.validity = False

        if not self.is_valid_password(psw):
            self.message = 'Password must contain uppercase and lowercase\
             latin letters [A-Z, a-z], numbers [0-9], and any of the special\
              characters [@#$%^&+=_]'
            self.validity = False

        if psw != psw2:
            self.message = 'Passwords don`t match'
            self.validity = False

        return DataError

    def is_valid_password(self, psw: str):
        return re.findall(self._password_pattern, psw)

    def is_valid_email(self, email: str):
        return re.search(self._email_pattern, email)


class UserData:
    # все пользователи, их инфа идет в таблицу users
    ip: str  # '94.140.141.124', request.remote
    user_cookies_uuid: str
    page: str

    def __init__(self, ip: str, user_cookies_uuid: str, page: str):
        self.ip = ip
        self.user_cookies_uuid = user_cookies_uuid
        self.page = page

    def get_user_info(self) -> dict:
        response = requests.get(url=f'http://ip-api.com/json/{self.ip}').json()
        return {
            'cookie': self.user_cookies_uuid,
            'ip': self.ip,
            'time': datetime.datetime.now().time(),
            'date': date.today(),
            'country': response['country'],
            'region': response['regionName'],
            'city': response['city'],
            'zip': response['zip'],
            'lat': response['lat'],
            'lon': response['lon'],
            'first_page': self.page
        }


@dataclass
class ClientData:
    login: str
    email: str
    password_hash: str
    cookies_uuid: str

    def get_client_info(self):
        return {
            'login': self.login,
            'email': self.email,
            'password_hash': self.password_hash,
            'cookies_uuid': self.cookies_uuid
        }


@dataclass
class Cookies:
    cookie = cookies.SimpleCookie()
    cookie_uuid: str

    def __init__(self, request):
        self.create_cookies(request)

    def create_cookies(self, request):
        if request.cookies.get('usr'):
            self.cookie['uuid'] = request.cookies.get('usr')
        else:
            self.cookie['uuid'] = uuid.uuid4().hex
        self.cookie['uuid']['path'] = request.host
        self.cookie['uuid']['domain'] = '127.0.0.1:5000'
        self.cookie['uuid']['secure'] = True
        self.cookie['uuid']['max-age'] = 2_419_000  # 28 days
        self.cookie['uuid']['httponly'] = True
        self.cookie['uuid']['expires'] = self.calculate_expire_time()

    @staticmethod
    def calculate_expire_time():
        expires_at_time = (
                    datetime.datetime.now() + datetime.timedelta(days=28)) \
            .strftime('%a, %d %b %Y %H:%M:%S')
        return expires_at_time

    def get_cookies(self):
        return self.cookie

    def get_str_cookies_uuid(self):
        return self.cookie['uuid'].value
