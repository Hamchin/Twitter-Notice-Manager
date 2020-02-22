from flask import Flask, request
import os, json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db_url = os.environ.get('DATABASE_URL') or "postgresql://localhost/notice"
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 通知テーブル
class Notice(db.Model):
    __tablename__ = 'notices'
    id = db.Column(db.Integer, primary_key = True)
    # 通知を受けたユーザーネーム
    receive_user = db.Column(db.String(), nullable = False)
    # 通知を送ったユーザーネーム
    send_user = db.Column(db.String(), nullable = False)
    # 通知対象のツイートID
    tweet_id = db.Column(db.String(), nullable = False)
    # 通知時間
    datetime = db.Column(db.String(), nullable = False)

# データを辞書型として取得
def get_dict(notice):
    data = {
        'receive_user': notice.receive_user,
        'send_user': notice.send_user,
        'tweet_id': notice.tweet_id,
        'datetime': notice.datetime
    }
    return data

# 全ての通知を取得
def get_notices():
    notices = db.session.query(Notice).all()
    data = [get_dict(notice) for notice in notices]
    return data

# 全ての通知を取得するエンドポイント
@app.route('/collect', methods = ['GET'])
def collect():
    notices = get_notices()
    res = json.dumps(notices, indent = 4)
    return res

# 通知を追加するエンドポイント
@app.route('/add', methods = ['POST'])
def add():
    req = request.get_json()
    notice = Notice()
    notice.receive_user = req['receive_user']
    notice.send_user = req['send_user']
    notice.tweet_id = req['tweet_id']
    notice.datetime = req['datetime']
    db.session.add(notice)
    db.session.commit()
    data = get_dict(notice)
    res = json.dumps(data, indent = 4)
    return res

# 全ての通知を削除するエンドポイント
@app.route('/delete', methods = ['POST'])
def delete():
    notices = get_notices()
    db.session.query(Notice).delete()
    db.session.commit()
    res = json.dumps(notices)
    return res
