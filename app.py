from flask import Flask, request
import os, json, datetime
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
        'id': notice.id,
        'receive_user': notice.receive_user,
        'send_user': notice.send_user,
        'tweet_id': notice.tweet_id,
        'datetime': notice.datetime
    }
    return data

# データの存在チェック
def exist(notice):
    count = db.session.query(Notice).filter(Notice.receive_user == notice.receive_user, Notice.send_user == notice.send_user, Notice.tweet_id == notice.tweet_id).count()
    return count > 0

# 指定日数以前の通知ID取得
def get_timeover_ids(day):
    ids = []
    notices = db.session.query(Notice).all()
    standard = datetime.datetime.now()
    for notice in notices:
        date = datetime.datetime.strptime(notice.datetime, "%Y-%m-%dT%H:%M:%S.000Z")
        date = date + datetime.timedelta(hours = 9)
        if standard - datetime.timedelta(days = day) > date: ids.append(notice.id)
    return ids

# 全ての通知を取得
@app.route('/notices', methods = ['GET'])
def get_notices():
    notices = db.session.query(Notice).all()
    data = [get_dict(notice) for notice in notices]
    data = sorted(data, key = lambda notice: notice['id'])
    res = json.dumps(data, indent = 4)
    return res

# 単体の通知を追加
# receive_user: 通知の受信ユーザー
# send_user: 通知の送信ユーザー
# tweet_id: ツイートID
# datetime: タイムスタンプ
@app.route('/notice', methods = ['GET'])
def get_notice():
    notice = Notice()
    notice.receive_user = request.args.get('receive_user')
    notice.send_user = request.args.get('send_user')
    notice.tweet_id = request.args.get('tweet_id')
    notice.datetime = request.args.get('datetime')
    if exist(notice): return ''
    db.session.add(notice)
    db.session.commit()
    data = get_dict(notice)
    res = json.dumps(data, indent = 4)
    return res

# 単体の通知を追加
# receive_user: 通知の受信ユーザー
# send_user: 通知の送信ユーザー
# tweet_id: ツイートID
# datetime: タイムスタンプ
@app.route('/notice', methods = ['POST'])
def add_notice():
    req = request.get_json()
    notice = Notice()
    notice.receive_user = req['receive_user']
    notice.send_user = req['send_user']
    notice.tweet_id = req['tweet_id']
    notice.datetime = req['datetime']
    if exist(notice): return ''
    db.session.add(notice)
    db.session.commit()
    data = get_dict(notice)
    res = json.dumps(data, indent = 4)
    return res

# 複数の通知を追加
# notices: 通知データの配列
@app.route('/notices', methods = ['POST'])
def add_notices():
    req = request.get_json()
    notices = req['notices']
    results = []
    for data in notices:
        notice = Notice()
        notice.receive_user = data['receive_user']
        notice.send_user = data['send_user']
        notice.tweet_id = data['tweet_id']
        notice.datetime = data['datetime']
        if exist(notice): continue
        db.session.add(notice)
        db.session.commit()
        results.append(data)
    res = json.dumps(results, indent = 4)
    return res

# 指定日数以前の通知を全て削除
# day: 指定日数
@app.route('/notices', methods = ['DELETE'])
def delete_notices():
    req = request.get_json()
    for ID in get_timeover_ids(req['day']):
        db.session.query(Notice).filter(Notice.id == ID).delete()
    db.session.commit()
    return ''

# 対象IDの通知を削除
# id: 対象ID
@app.route('/notice', methods = ['DELETE'])
def delete_notice():
    req = request.get_json()
    db.session.query(Notice).filter(Notice.id == req['id']).delete()
    db.session.commit()
    return ''

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 8080, debug = True)
