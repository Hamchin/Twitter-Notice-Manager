import sqlite3, os, json, datetime
from flask import Flask, request, render_template
from flask_cors import CORS
from requests_oauthlib import OAuth1Session
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

DATABASE_PATH = './notice.db'
BACKUP_PATH = './backup.db'
load_dotenv()

CK = os.getenv('TWITTER_CONSUMER_KEY')
CS = os.getenv('TWITTER_CONSUMER_SECRET')
AT = os.getenv('TWITTER_ACCESS_TOKEN')
AS = os.getenv('TWITTER_ACCESS_SECRET')
twitter = OAuth1Session(CK, CS, AT, AS)

# 通知データ
class Notice():
    def __init__(self, receiver_id, sender_id, tweet_id, timestamp):
        self.receiver_id = receiver_id
        self.sender_id = sender_id
        self.tweet_id = tweet_id
        self.timestamp = timestamp

# バックアップ (1回/日)
def backup(connection):
    now_date = datetime.datetime.now()
    backup_timestamp = os.path.getctime(DATABASE_PATH) if os.path.exists(BACKUP_PATH) else 0
    backup_date = datetime.datetime.fromtimestamp(backup_timestamp)
    is_same_year = now_date.year == backup_date.year
    is_same_month = now_date.month == backup_date.month
    is_same_day = now_date.day == backup_date.day
    if is_same_year and is_same_month and is_same_day: return
    backup_connection = sqlite3.connect(BACKUP_PATH)
    connection.backup(backup_connection)
    backup_connection.close()

# データベース操作用デコレーター
def database(func):
    def wrapper(*args, **kwargs):
        # データベース接続
        connection = sqlite3.connect(DATABASE_PATH)
        connection.row_factory = sqlite3.Row
        # カーソル作成
        cursor = connection.cursor()
        # 処理の実行
        kwargs['cursor'] = cursor
        res = func(*args, **kwargs)
        # データベースの保存
        connection.commit()
        # バックアップ
        backup(connection)
        # データベースの接続を閉じる
        connection.close()
        return res
    return wrapper

# テーブル作成
@database
def create(cursor = None):
    # receiver_id : 通知を受けたユーザーID
    # sender_id : 通知を送ったユーザーID
    # tweet_id : 通知対象のツイートID
    # timestamp : タイムスタンプ
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notices (
        id INTEGER PRIMARY KEY,
        receiver_id TEXT,
        sender_id TEXT,
        tweet_id TEXT,
        timestamp INTEGER
    )
    """)

# ユーザーネームからユーザー取得
def get_user(name):
    url = "https://api.twitter.com/1.1/users/show.json"
    params = {
        'screen_name': name,
        'include_entities': False
    }
    res = twitter.get(url, params = params, timeout = 10)
    if res.status_code != 200: return {}
    return json.loads(res.text)

# IDリストからユーザーリスト取得
def get_users(user_ids):
    url = "https://api.twitter.com/1.1/users/lookup.json"
    params = {
        'user_id': ','.join(user_ids),
        'include_entities': False
    }
    res = twitter.get(url, params = params, timeout = 10)
    if res.status_code != 200: return []
    return json.loads(res.text)

# 重複チェック
@database
def duplicate(notice, cursor = None):
    sql = "SELECT * FROM notices WHERE receiver_id = ? AND sender_id = ? AND tweet_id = ?"
    cursor.execute(sql, (notice.receiver_id, notice.sender_id, notice.tweet_id))
    notices = [dict(notice) for notice in cursor.fetchall()]
    return len(notices) > 0

# 複数の通知取得
@database
def get_notices(size, cursor = None):
    if size == 0:
        cursor.execute("SELECT * FROM notices ORDER BY timestamp DESC")
    else:
        cursor.execute("SELECT * FROM notices ORDER BY timestamp DESC LIMIT ?", (size,))
    notices = [dict(notice) for notice in cursor.fetchall()]
    return notices

# 単体の通知取得
@database
def get_notice(id, cursor = None):
    cursor.execute("SELECT * FROM notices WHERE id = ?", (id,))
    data = cursor.fetchone()
    if data is None: return None
    notice = dict(data)
    return notice

# 単体の通知挿入
@database
def insert_notice(notice, cursor = None):
    sql = "INSERT INTO notices (receiver_id, sender_id, tweet_id, timestamp) VALUES (?, ?, ?, ?)"
    cursor.execute(sql, (notice.receiver_id, notice.sender_id, notice.tweet_id, notice.timestamp))

# 単体の通知削除
@database
def delete_notice(id, cursor = None):
    cursor.execute("DELETE FROM notices WHERE id = ?", (id,))

# トップページ
@app.route('/')
def index():
    notices = get_notices(size = 100)
    user_ids = [notice['receiver_id'] for notice in notices] + [notice['sender_id'] for notice in notices]
    user_ids = list(set(user_ids))
    users = get_users(user_ids)
    users = {user['id_str']: {'name': user['name'], 'screen_name': user['screen_name']} for user in users}
    default_user = {'name': '', 'screen_name': ''}
    for notice in notices:
        notice['receiver'] = users.get(notice['receiver_id'], default_user)
        notice['sender'] = users.get(notice['sender_id'], default_user)
        date = datetime.datetime.fromtimestamp(notice['timestamp'])
        notice['datetime'] = date.strftime("%Y-%m-%d · %H:%M:%S")
    return render_template('index.html', notices = notices)

# 通知取得API
# size: 通知取得数
@app.route('/notices', methods = ['GET'])
def api_get_notices():
    size = request.args.get('size', 10, type = int)
    notices = get_notices(size)
    return json.dumps(notices, indent = 4)

# 通知追加API
# receiver: 通知の受信ユーザー
# sender: 通知の送信ユーザー
# tweet_id: ツイートID
# timestamp: タイムスタンプ
@app.route('/notice/create', methods = ['POST'])
def api_create_notice():
    data = request.get_json()
    # パラメータ読み込み
    receiver = data.get('receiver')
    sender = data.get('sender')
    tweet_id = data.get('tweet_id')
    timestamp = data.get('timestamp')
    if not (receiver and sender and tweet_id and timestamp):
        res = {'status': 'MISSING_PARAMS'}
        return json.dumps(res, indent = 4)
    # ユーザーネームからユーザーID取得
    receiver_id = get_user(receiver).get('id_str')
    sender_id = get_user(sender).get('id_str')
    if not (receiver_id and sender_id):
        res = {'status': 'INVALID_USER'}
        return json.dumps(res, indent = 4)
    # 通知追加
    notice = Notice(receiver_id, sender_id, tweet_id, timestamp)
    if duplicate(notice):
        res = {'status': 'DUPLICATE_NOTICE'}
        return json.dumps(res, indent = 4)
    insert_notice(notice)
    res = {'status': 'SUCCESS'}
    return json.dumps(res, indent = 4)

# 通知挿入API
# receiver_id: 通知の受信ユーザーID
# sender_id: 通知の送信ユーザーID
# tweet_id: ツイートID
# timestamp: タイムスタンプ
@app.route('/notice/insert', methods = ['POST'])
def api_insert_notice():
    data = request.get_json()
    # パラメータ読み込み
    receiver_id = data.get('receiver_id')
    sender_id = data.get('sender_id')
    tweet_id = data.get('tweet_id')
    timestamp = data.get('timestamp')
    if not (receiver_id and sender_id and tweet_id and timestamp):
        res = {'status': 'MISSING_PARAMS'}
        return json.dumps(res, indent = 4)
    # 通知追加
    notice = Notice(receiver_id, sender_id, tweet_id, timestamp)
    if duplicate(notice):
        res = {'status': 'DUPLICATE_NOTICE'}
        return json.dumps(res, indent = 4)
    insert_notice(notice)
    res = {'status': 'SUCCESS'}
    return json.dumps(res, indent = 4)

# 通知削除API
# id: 対象ID
@app.route('/notice/delete/<id>', methods = ['POST'])
def api_delete_notice(id):
    notice = get_notice(id)
    if notice is None:
        res = {'status': 'NOT_EXIST_NOTICE'}
        return json.dumps(res, indent = 4)
    delete_notice(id)
    res = {'status': 'SUCCESS'}
    return json.dumps(res, indent = 4)

if __name__ == "__main__":
    create()
    app.run(host = '0.0.0.0', port = 8000, debug = True)
