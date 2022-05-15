import json
from pony.orm import *


with open("general_config.json", "r") as config:
    db_config = json.load(config)['DATABASE']

db = Database()

db.bind(provider='postgres',
        user=db_config['USER'],
        password=db_config['PASSWORD'],
        host=db_config['HOST'],
        dbname=db_config['DB_NAME'])
