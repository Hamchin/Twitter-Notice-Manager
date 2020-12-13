import twitter, table, json

# オブジェクトからユーザーIDを取得する
def get_user_id(data, id_key, name_key):
    user_id = data.get(id_key) or ''
    if user_id != '': return user_id
    screen_name = data.get(name_key) or ''
    if screen_name == '': return ''
    user = twitter.get_user(screen_name = screen_name)
    if user is None: return ''
    return user['id_str']

# レスポンス用に通知をマッピングする
def mapping(notice):
    data = {}
    if 'ReceiverID' in notice:
        data['receiver_id'] = notice['ReceiverID']
    if 'SenderID' in notice:
        data['sender_id'] = notice['SenderID']
    if 'TweetID' in notice:
        data['tweet_id'] = notice['TweetID']
    if 'Receiver' in notice:
        data['receiver'] = notice['Receiver']
    if 'Sender' in notice:
        data['sender'] = notice['Sender']
    if 'Tweet' in notice:
        data['tweet'] = notice['Tweet']
    if 'Timestamp' in notice:
        data['timestamp'] = int(notice['Timestamp'])
    return data

# レスポンスを生成する
def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(body)
    }

# ステータスからレスポンスを生成する
def response_from_status(status):
    body = {'status': status}
    if status == 'OK':
        return response(200, body)
    elif status == 'INTERNAL_ERROR':
        return response(500, body)
    else:
        return response(400, body)

def lambda_handler(event, context):
    path = event.get('path') or ''
    method = event.get('httpMethod') or ''
    params = event.get('queryStringParameters') or {}
    body = event.get('body')
    body = json.loads(body) if body else {}
    # 複数の通知を取得する
    # receiver_id (receiver_name): String
    # size: Integer
    # mode: String
    if path == '/notices' and method == 'GET':
        receiver_id = get_user_id(params, 'receiver_id', 'receiver_name')
        size = int(params.get('size') or 10)
        mode = params.get('mode') or ''
        notices = table.query(receiver_id, size, mode)
        notices = [mapping(notice) for notice in notices]
        return response(200, notices)
    # 通知を追加/更新する
    # receiver_id (receiver_name): String
    # sender_id (sender_name): String
    # tweet_id: String
    # timestamp: Integer
    elif path == '/notice/update' and method == 'POST':
        receiver_id = get_user_id(body, 'receiver_id', 'receiver_name')
        sender_id = get_user_id(body, 'sender_id', 'sender_name')
        tweet_id = body.get('tweet_id') or ''
        timestamp = int(body.get('timestamp') or 0)
        status = table.put_item(receiver_id, sender_id, tweet_id, timestamp)
        return response_from_status(status)
    # 通知を削除する
    # receiver_id (receiver_name): String
    # sender_id (sender_name): String
    # tweet_id: String
    elif path == '/notice/delete' and method == 'POST':
        receiver_id = get_user_id(body, 'receiver_id', 'receiver_name')
        sender_id = get_user_id(body, 'sender_id', 'sender_name')
        tweet_id = body.get('tweet_id') or ''
        status = table.delete_item(receiver_id, sender_id, tweet_id)
        return response_from_status(status)
    return response(400, None)
