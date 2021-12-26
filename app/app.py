from flask import Flask,render_template,request,url_for,redirect,session
from app.config import SALT, SECRET_KEY, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, MAIL_USE_TLS, MAIL_USE_SSL
from models.models import User,Team,Game,UserWatchingLog
from models.database import db_session
from datetime import datetime
# ハッシュ化されたパスワード生成のためにimport
from hashlib import sha256
# 予約語or_モジュールのimport
from sqlalchemy import and_,or_
# flask_mailモジュールから、Mailインスタンスを利用を宣言
from flask_mail import Mail, Message
# Flask-APScheduler の利用を宣言
# from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
# import zoneinfo
import zoneinfo
# import datetime
import datetime

# Flaskモジュール生成
app = Flask(__name__)

# Mailインスタンスを生成
app.config['MAIL_SERVER']= MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = MAIL_USE_SSL
mail = Mail(app)

# Schedulerのインスタンスを作成
# app.config['SCHEDULER_API_ENABLED'] = True
# scheduler = APScheduler()


# セッション情報の暗号化
app.secret_key = SECRET_KEY

# # ログイン確認を共通化
# def is_login():
#     if "email" in session:
#         exit()
#     else:
#         status = "need_to_login"
#         return redirect(url_for("index",status=status))
        

# scheduler処理

# # 全ユーザーを取得しそれぞれにnotice_timeを発行する
# # session から ログイン中のuser を取得
# user = User.query.filter_by(email=session["email"]).first()
# # お気に入りチームを取得する
# favo_teams_id = user.favo_teams_id
# # お気に入りチームの最新の試合を取得する
# latest_game = Game.query.filter(or_(Game.home_team_id==favo_teams_id,Game.away_team_id==favo_teams_id)).order_by(Game.game_date.desc()).first()
# print(latest_game)
# # ゲームの終了日時の5分後のdatetimeを返す
# notice_timedate = latest_game.game_date + datetime.timedelta(days=19,hours=10,minutes=16)

def sendmail():
    with app.app_context():
        notice = Message("【j-ikitai】Notification",
            sender="m0naaa0u@gmail.com",
            # 今後は、会員ユーザーごとにジョブを発行するようにする
            recipients = ["m0naaa0u@gmail.com"]
        )
        notice.body = "It's time to record your watching logs of today's game!"
        mail.send(notice)
# scheduler を使う
scheduler = BackgroundScheduler({'apscheduler.timezone': 'Asia/Tokyo'})
# scheduler.add_job(sendmail,'cron',year=notice_timedate.year,month=notice_timedate.month,day=notice_timedate.day,hour=notice_timedate.hour,minute=notice_timedate.minute)
scheduler.add_job(sendmail,'cron',hour=17,minute=18)
scheduler.start()


# route処理
@app.route("/")
def top():
    return redirect("index")

# トップページ処理
@app.route("/index")
def index():
    status = request.args.get("status")
    return render_template("index.html",status=status)

# / でのログイン確認
@app.route("/login", methods=["post"])
def login():
    # ログインフォームに入力したusernameを取得
    email = request.form["email"]
    # 対象のusernameのレコードを抽出
    user = User.query.filter_by(email=email).first()
    # 対象のusernameのレコードが存在すれば、次にパスワードの確認に進む
    if user:
        password = request.form["password"]
        hashed_password = sha256((email + password + SALT).encode("utf-8")).hexdigest()
        # ハッシュ化したパスワード同士が一致すれば、セッションをcookieに記録して/index にリダイレクト
        if user.hashed_password == hashed_password:
            session["email"] = email
            # ログイン成功したらメールを送付する
            msg = Message("Login successfully",
                sender="m0naaa0u@gmail.com",
                recipients = ["m0naaa0u@gmail.com"]
            )
            msg.body = "Thank you for using app.Login successfully"
            # mail.send(msg)
            return redirect("/games")
        else:
            # パスワードエラーのステータスを格納
            status = "wrong_password"
            # ハッシュ化したパスワード同士が一致しなれば、パスワードが間違っていることを伝える
            return redirect(url_for("index",status=status))
    else:
        # パスワードエラーのステータスを格納
        status = "user_not_found"
        # 対象のusernameのレコードが存在しなければ、ユーザーが見つからない旨を返す
        return redirect(url_for("index",status=status))

# /register 表示
@app.route("/register")
def register():
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
    # 試合一覧にリダイレクト
    return redirect("/games")

# ログアウト
@app.route("/logout")
def logout():
    session.pop("email",None)
    return redirect("/")


@app.route("/games",methods=["get","post"])
def games():
    # ログインしていなければ、ログイン画面に遷移させる
    if "email" in session:
        # session から ログイン中のuser_id を取得
        user = User.query.filter_by(email=session["email"]).first()
        # username を取得
        user_email = user.email
        # お気に入りチームを取得する
        favo_teams_id = user.favo_teams_id
        # お気に入りチームの全試合を取得する
        favo_all_games = Game.query.filter(or_(Game.home_team_id==favo_teams_id,Game.away_team_id==favo_teams_id)).all()
        # 全チーム取得
        teams = Team.query.all()
        # hogehoge
        return render_template("games.html",favo_teams_id=favo_teams_id,favo_all_games=favo_all_games,teams=teams,user_email=user_email)
    else:
        status = "need_to_login"
        return redirect(url_for("index",status=status))

# To add variable parts to a URL
# https://qiita.com/5zm/items/c8384aa7b7aae924135c
@app.route("/games/log/<int:game_id>/edit",methods=["get","post"])
def edit(game_id):
    # ログインしていなければ、ログイン画面に遷移させる
    if "email" in session:
        # ログを残したい試合を取得
        log_game = Game.query.filter_by(id=game_id).first()
        # ホームチーム名取得
        home_team = Team.query.filter_by(id=log_game.home_team_id).first()
        # アウェイチーム名取得
        away_team = Team.query.filter_by(id=log_game.away_team_id).first()
        # すでに観戦ログがあれば、観戦ログを取得して送る
        user_id = User.query.filter_by(email=session["email"]).first().id
        user_log = UserWatchingLog.query.filter(and_(UserWatchingLog.game_id==game_id,UserWatchingLog.user_id==user_id)).first()
        return render_template("edit_log.html",log_game=log_game,home_team=home_team,away_team=away_team,game_id=game_id,user_log=user_log)
    else:
        status = "need_to_login"
        return redirect(url_for("index",status=status))

@app.route("/games/log/<int:game_id>/add",methods=["get","post"])
def add(game_id):
    # ログインしていなければ、ログイン画面に遷移させる
    if "email" in session:
        # ログを残したい試合を取得
        log_game = Game.query.filter_by(id=game_id).first()
        # ホームチーム名取得
        home_team = Team.query.filter_by(id=log_game.home_team_id).first()
        # アウェイチーム名取得
        away_team = Team.query.filter_by(id=log_game.away_team_id).first()
        return render_template("add_log.html",log_game=log_game,home_team=home_team,away_team=away_team,game_id=game_id)
    else:
        status = "need_to_login"
        return redirect(url_for("index",status=status))

@app.route("/games/log/<int:game_id>",methods=["get"])
def log(game_id):
    # ログインしていなければ、ログイン画面に遷移させる
    if "email" in session:
        # ログを残したい試合を取得
        log_game = Game.query.filter_by(id=game_id).first()
        # ホームチーム名取得
        home_team = Team.query.filter_by(id=log_game.home_team_id).first()
        # アウェイチーム名取得
        away_team = Team.query.filter_by(id=log_game.away_team_id).first()
        # session から user_id を取得
        user_id = User.query.filter_by(email=session["email"]).first().id
        # 観戦ログ取得
        user_log = UserWatchingLog.query.filter(and_(UserWatchingLog.user_id==user_id, UserWatchingLog.game_id==game_id)).first()
        return render_template("log.html",log_game=log_game,home_team=home_team,away_team=away_team,user_log=user_log)
    else:
        status = "need_to_login"
        return redirect(url_for("index",status=status))

@app.route("/addlog", methods=["post"])
def addlog():
    # ログインしていなければ、ログイン画面に遷移させる
    if "email" in session:
        # session から user_id を取得
        user_id = User.query.filter_by(email=session["email"]).first().id
        # form から game_id を hidden で取得
        game_id = request.form["game_id"]
        # form から status を取得
        status = request.form["status"]
        # form から comment を取得
        comment = request.form["comment"]
        updated_at = datetime.now()
        # user_watching_logテーブルにレコードを追加
        new_user_watching_log = UserWatchingLog(user_id,game_id,status,comment)
        db_session.add(new_user_watching_log)
        db_session.commit()
        return redirect("/games/log/" + game_id)
    else:
        status = "need_to_login"
        return redirect(url_for("index",status=status))

@app.route("/editlog", methods=["post"])
def editlog():
    # ログインしていなければ、ログイン画面に遷移させる
    if "email" in session:
        # form から game_id を hidden で取得
        game_id = request.form["game_id"]
        # すでに観戦ログがあれば、観戦ログを取得して送る
        user_id = User.query.filter_by(email=session["email"]).first().id
        user_log = UserWatchingLog.query.filter(and_(UserWatchingLog.game_id==game_id,UserWatchingLog.user_id==user_id)).first()
        # status を更新
        user_log.status = request.form["status"]
        # commnet を更新
        user_log.comment = request.form["comment"]
        db_session.commit()
        return redirect("/games/log/" + game_id)
    else:
        status = "need_to_login"
        return redirect(url_for("index",status=status))

# import 制御
if __name__ == "__main__":
    app.run(debug=True)