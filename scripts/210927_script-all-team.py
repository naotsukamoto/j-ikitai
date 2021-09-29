from models.models import Team
from models.database import db_session

teams = ['北海道コンサドーレ札幌','柏レイソル','川崎フロンターレ','横浜ＦＣ','清水エスパルス','ガンバ大阪','ヴィッセル神戸','徳島ヴォルティス','サガン鳥栖','ベガルタ仙台','浦和レッズ','ＦＣ東京','横浜Ｆ・マリノス','湘南ベルマーレ','名古屋グランパス','セレッソ大阪','サンフレッチェ広島','アビスパ福岡','大分トリニータ']

for team in teams:
    db_session.add(Team(1,team))

db_session.commit()