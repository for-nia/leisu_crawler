# coding=utf8

from mongoengine import *

connect(host=r'mongodb://ls:ls_data@localhost:27017/test')

class Match(Document):
    match_id = IntField(primary_key=True)
    home_name = StringField()
    away_name = StringField()
    home_head = StringField()
    away_head = StringField()
    begin_time = DateTimeField()

