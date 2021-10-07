from flask import Flask,render_template,request,url_for,redirect,session
from app.config import SALT
from models.models import User,Team,Game
from models.database import db_session
# ハッシュ化されたパスワード生成のためにimport
from hashlib import sha256
# 予約語or_モジュールのimport
from sqlalchemy import or_

# Flaskモジュール生成
app = Flask(__name__)

# /処理
@app.route("/")
def top():
    return "hello world"

# /register 表示
@app.route("/register")
def index():
    all_teams = Team.query.all()
    return render_template("signup.html",all_teams=all_teams)

@app.route("/signup",methods=["post"])
def signup():
    email = request.form["email"]
    password = request.form["password"]
    hashed_password = sha256((email + password + SALT).encode("utf-8")).hexdigest()
    favo_teams_id = request.form["favo_team_id"]
    nickname = request.form["nickname"]
    new_user = User(email, hashed_password, nickname, favo_teams_id)
    db_session.add(new_user)
    db_session.commit()
    # お気に入りチームをパラメータとして引き継ぐ
    return redirect(url_for("games",favo_teams_id=favo_teams_id))

@app.route("/games",methods=["get","post"])
def games():
    favo_teams_id = request.args.get("favo_teams_id")
    # お気に入りチームの全試合を取得する
    favo_all_games = Game.query.filter(or_(Game.home_team_id==favo_teams_id,Game.away_team_id==favo_teams_id)).all()
    # 全チーム取得
    teams = Team.query.all()
    # hogehoge
    return render_template("games.html",favo_teams_id=favo_teams_id,favo_all_games=favo_all_games,teams=teams)

# To add variable parts to a URL
# https://qiita.com/5zm/items/c8384aa7b7aae924135c
@app.route("/games/log/<int:game_id>",methods=["get","post"])
def log(game_id):
    # ログを残したい試合を取得
    log_game = Game.query.filter_by(id=game_id).first()
    # ホームチーム名取得
    home_team = Team.query.filter_by(id=log_game.home_team_id).first()
    # アウェイチーム名取得
    away_team = Team.query.filter_by(id=log_game.away_team_id).first()
    return render_template("log.html",log_game=log_game,home_team=home_team,away_team=away_team)


# import 制御
if __name__ == "__main__":
    app.run(debug=True)