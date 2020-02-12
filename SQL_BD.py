from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,ForeignKey,Float
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from random import randint
from sqlalchemy.orm import relationship
import json
import sys
import codecs



base = declarative_base()

class User(base):
    __tablename__ = "user"
    uid = Column(Integer, primary_key=True)
    team_number3 = Column(Integer, ForeignKey('team.team_id')) #вначале таблица, потом поле
    name = Column(String)
    bal = Column(Float)

    def __init__(self, uid, name, team, ball=0):
        self.uid = uid
        self.name = name
        self.team = team
        self.ball = ball
    def __str__(self):
        return self.name.lower()

class Team(base):
    __tablename__ = "team"
    team_name = Column(String)
    team_id = Column(Integer, primary_key=True)
    bal = Column(Integer)
    users = relationship('User', backref='team')
    def __init__(self, team_id, team_name,bal=0): #  говорим как конструировать
        self.team_id = team_id
        self.bal = bal
        self.team_name = team_name
    def __str__(self):
        return self.team_name #то, что будем выводить


sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

engine = create_engine("sqlite:///tasks.db",echo=True)
base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
s = Session()

def insert(t):
    s.add(t)
    s.commit()
def delete(uid):
    s.query(User).filter(User.id == uid).delete()
    s.commit()
def change(uid, team):
    t = s.query(User).filter(User.id == uid).delete().first()
    t.team = team
    s.commit
def insert_Team(team_id, team_name):
    team1 = Team(team_id, team_name)
    insert(team1)
def insert_user(uid, name, team):
    user=User(uid, name, team)
    insert(user)
def file_pars(file_name):
    with open(file_name, 'r') as read_file:
        team = json.load(read_file)
        for i in team["TEAMS"]:
            d=Team(i["Team_id"],i["TEAM_NAME"])
            s.add(d)
    s.commit()#сохраняет изменения
file_pars("team1.json")
t = s.query(Team)

for i in t: #в i  определнный объект из базы
    k=i.encode('utf-8')
    print(k)

