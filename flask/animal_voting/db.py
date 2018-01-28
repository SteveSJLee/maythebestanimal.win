from peewee import Model
from peewee import CharField
from peewee import IntegrityError
from peewee import MySQLDatabase
from peewee import OperationalError
from os import environ


db = MySQLDatabase(environ['FLASK_DB_NAME'],
                   user=environ['FLASK_DB_USER'],
                   password=environ['FLASK_DB_PASS'],
                   host=environ['FLASK_DB_HOST'])

# Peewee database exception classes, used in main application
db_exceptions = {'IntegrityError': IntegrityError,
                 'OperationalError': OperationalError}


class BaseModel(Model):
    class Meta:
        database = db


class Person(BaseModel):
    person_name = CharField(unique=True)
    favorite_color = CharField()
    favorite_animal = CharField()
