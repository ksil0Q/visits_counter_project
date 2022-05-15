from collections import Counter
from datetime import datetime, timedelta
from models import Client, User
from pony.orm import *


class UserManager(object):
    @db_session
    def get_stat_by_country(self, country: str):
        return Counter([p.country for p in User.select()])[country]

    @db_session
    def get_country_stat(self):
        return Counter([p.country for p in User.select()])

    @db_session
    def get_stat_by_date(self, some_date: datetime):
        return Counter([p.connection_date for p in User.select()])[some_date]

    @db_session
    def get_gen_stat_by_dates(self):
        return Counter([p.connection_date for p in User.select()])

    @db_session
    def get_stat_by_last_half_hour(self):
        half_hour = (datetime.now() - timedelta(minutes=30)).time()
        today_date = datetime.today().date()

        return len([p.time for p in User.select() if p.time > half_hour and
                    p.connection_date == today_date])

    @db_session
    def get_stat_by_last_day(self):
        today_date = datetime.today().date()
        return dict(select((p.time.hour, count(p)) for p in User.select()
                           if p.connection_date == today_date))

    @db_session
    def get_stat_by_last_month(self):
        month = (datetime.now() - timedelta(days=datetime.now().day)).date()
        return Counter([p.connection_date for p in User.select()
                        if p.connection_date > month])

    @db_session
    def get_stat_about_unique_users(self):
        return select(
            p.cookies_uuid for p in User.select()).without_distinct().count()

    @db_session
    def get_pages_stat(self):
        return Counter([p.first_page for p in User.select()])

    @db_session
    def get_logon_pages_stat(self):
        return Counter([p.first_page for p in User.select()])


class ClientManager(object):
    @db_session
    def get_stat_about_registered_users(self):
        return select(p for p in Client.select()).count()
