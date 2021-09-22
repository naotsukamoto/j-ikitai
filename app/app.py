from flask import Flask

# Flaskモジュール生成
app = Flask(__name__)

# /処理
@app.route("/")
def index():
    return "hello world"

# import 制御
if __name__ == "__main__":
    app.run(debug=True)