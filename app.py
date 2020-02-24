from flask import Flask, request, render_template, redirect, url_for
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
    def get_dict(self):
        data = {
            'id': self.id,
            'receive_user': self.receive_user,
            'send_user': self.send_user,
            'tweet_id': self.tweet_id,
            'datetime': self.datetime
        }
        return data

# 日付整形
def format_date(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.000Z")
    date = date + datetime.timedelta(hours = 9)
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    return date

# 重複チェック
def exist(notice):
    count = db.session.query(Notice).filter(
        Notice.receive_user == notice.receive_user,
        Notice.send_user == notice.send_user,
        Notice.tweet_id == notice.tweet_id
    ).count()
    return count > 0

# 通知追加
def add_notice(data):
    notice = Notice()
    receive_user = data.get('receive_user')
    send_user = data.get('send_user')
    tweet_id = data.get('tweet_id')
    date = data.get('datetime')
    if not (receive_user and send_user and tweet_id and date): return {}
    date = format_date(date)
    notice.receive_user = receive_user
    notice.send_user = send_user
    notice.tweet_id = tweet_id
    notice.datetime = date
    if exist(notice): return {}
    db.session.add(notice)
    db.session.commit()
    return notice.get_dict()

# 通知取得
def get_notices(size):
    notices = db.session.query(Notice).order_by(Notice.id.desc()).limit(size).all()
    notices = [notice.get_dict() for notice in notices]
    notices = sorted(notices, key = lambda notice: notice['id'])
    return notices

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

# トップページ
@app.route('/')
def index():
    notices = get_notices(100)
    return render_template('index.html', notices = reversed(notices))

# 通知追加ルーティング
@app.route('/notice', methods = ['POST'])
def post_notice():
    notice = add_notice(request.form)
    return redirect(url_for('index'))

# 通知取得API
# size: 通知取得数
@app.route('/api/notices', methods = ['GET'])
def api_get_notices():
    size = request.args.get('size', 10)
    notices = get_notices(size)
    return json.dumps(notices, indent = 4)

# 通知追加API
# receive_user: 通知の受信ユーザー
# send_user: 通知の送信ユーザー
# tweet_id: ツイートID
# datetime: タイムスタンプ
@app.route('/api/notice/create', methods = ['GET'])
def api_create_notice():
    notice = add_notice(request.args)
    return json.dumps(notice, indent = 4)

# 通知追加API
# receive_user: 通知の受信ユーザー
# send_user: 通知の送信ユーザー
# tweet_id: ツイートID
# datetime: タイムスタンプ
@app.route('/api/notice', methods = ['POST'])
def api_post_notice():
    notice = add_notice(request.get_json())
    return json.dumps(notice, indent = 4)

# 通知削除API
# id: 対象ID
@app.route('/api/notice', methods = ['DELETE'])
def delete_notice():
    req = request.get_json()
    data = db.session.query(Notice).filter(Notice.id == req['id']).first()
    if data is None: return {}
    notice = data.get_dict()
    db.session.delete(data)
    db.session.commit()
    return json.dumps(notice, indent = 4)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 8080, debug = True)
