from sqlalchemy import Column, Integer, DateTime, String, Text, ForeignKey
from sqlalchemy.orm import relationship,backref
from models.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key = True)
    email = Column(String(128),unique = True, nullable = False)
    hashed_password = Column(String(128),unique = True, nullable = False)
    nickname = Column(String(128),unique = True)
    favo_teams_id = Column(Integer,ForeignKey("teams.id"),nullable = False)
    session_time = Column(DateTime)
    status = Column(Integer)
    created_at = Column(DateTime,default = datetime.now())
    updated_at = Column(DateTime)

    teams = relationship("Team", backref="user")

    def __init__(self, email,hashed_password,nickname,favo_team_id,session_time,status,created_at,updated_at):
        self.email = email
        self.hashed_password = hashed_password
        self.nickname = nickname
        self.favo_team_id = favo_team_id
        self.session_time = session_time
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<Email %r>' % (self.email)

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer,primary_key = True)
    season = Column(Integer)
    team_name = Column(String(128),unique = True)
    created_at = Column(DateTime,default = datetime.now())

    def __init__(self, season, team_name, created_at):
        self.season = season
        self.team_name = team_name
        self.created_at = created_at


    def __repr__(self):
        return '<TeamName %r>' % (self.team_name)