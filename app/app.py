from flask import Flask,render_template

# Flaskモジュール生成
app = Flask(__name__)

# /処理
@app.route("/")
def index():
    return "hello world"

# signup
@app.route("/register")
def signup():
    return render_template("signup.html")

# import 制御
if __name__ == "__main__":
    app.run(debug=True)