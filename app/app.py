from flask import Flask,render_template,request,url_for,redirect,session
from app.config import SALT
from models.models import User,Team
from models.database import db_session
# ハッシュ化されたパスワード生成のためにimport
from hashlib import sha256

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
    return redirect(url_for("games"))

@app.route("/games")
def games():
    return render_template("games.html")

# import 制御
if __name__ == "__main__":
    app.run(debug=True)