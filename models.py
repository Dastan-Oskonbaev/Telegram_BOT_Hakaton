import peewee
from peewee import *

db = SqliteDatabase('complaints.db')


class Person(Model):
    id = peewee.AutoField(unique=True)
    telegram_id = peewee.IntegerField(unique=True)
    first_name = CharField()
    last_name = CharField()
    email = CharField(unique=True)
    password = CharField()
    age = IntegerField()
    male = CharField()
    city = CharField()

    class Meta:
        database = db


class Complaint(Model):
    person = ForeignKeyField(Person, backref='complaints')
    description = TextField()
    date_time = DateTimeField()

    class Meta:
        database = db


def initialize_db():
    db.connect()
    db.create_tables([Person, Complaint])

initialize_db()