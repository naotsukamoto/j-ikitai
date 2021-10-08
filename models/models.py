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
    user_watching_logs = relationship("UserWatchingLog", backref="user")

    def __init__(self, email=None,hashed_password=None,nickname=None,favo_teams_id=None,session_time=None,status=None,created_at=None,updated_at=None):
        self.email = email
        self.hashed_password = hashed_password
        self.nickname = nickname
        self.favo_teams_id = favo_teams_id
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

    def __init__(self, season=None, team_name=None, created_at=None):
        self.season = season
        self.team_name = team_name
        self.created_at = created_at


    def __repr__(self):
        return '<TeamName %r>' % (self.team_name)

class Game(Base):
    __tablename__ = "games"
    id = Column(Integer,primary_key = True)
    game_date = Column(DateTime)
    home_team_id = Column(Integer,ForeignKey("teams.id"),nullable = False)
    away_team_id = Column(Integer,ForeignKey("teams.id"),nullable = False)
    home_team_score = Column(Integer)
    away_team_score = Column(Integer)
    created_at = Column(DateTime,default = datetime.now())

    # https://docs.sqlalchemy.org/en/14/orm/join_conditions.html
    # home_team = relationship("Team")
    # away_team = relationship("Team")

    def __init__(self, game_date=None, home_team_id=None,away_team_id=None, home_team_score=None,away_team_score=None,created_at=None):
        self.game_date = game_date
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.home_team_score = home_team_score
        self.away_team_score = away_team_score
        self.created_at = created_at

    def __repr__(self):
        return '<GameName %r>' % (self.game_date)

    user_watching_logs = relationship("UserWatchingLog",backref="game")

class UserWatchingLog(Base):
    __tablename__ = "user_watching_logs"
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable = False)
    game_id = Column(Integer, ForeignKey("games.id"),nullable = False)
    status = Column(Integer)
    comment = Column(Text)
    created_at = Column(DateTime, default = datetime.now())
    updated_at = Column(DateTime)

    def __int__(self, user_id=None, game_id=None, status=None, commnet=None, created_at=None, updated_at=None):
        self.user_id = user_id
        self.game_id = game_id
        self.status = status
        self.comment = comment
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<UserWatchingLog %r>' % (self.status)



    