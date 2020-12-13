import boto3, twitter
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TwitterNotice')

# 通知を取得する
def get_item(receiver_id, sender_id, tweet_id):
    for param in [receiver_id, sender_id, tweet_id]:
        if not param: return None
    response = table.get_item(
        Key = {'ID': f'{receiver_id}-{sender_id}-{tweet_id}'},
        ProjectionExpression = 'ReceiverID, SenderID, TweetID, #Timestamp',
        ExpressionAttributeNames = {'#Timestamp': 'Timestamp'},
    )
    return response.get('Item')

# IDをオブジェクトへ変換する
def expand_notices(notices):
    receiver_ids = [notice['ReceiverID'] for notice in notices]
    sender_ids = [notice['SenderID'] for notice in notices]
    user_ids = list(set(receiver_ids + sender_ids))
    users = twitter.get_users(user_ids = user_ids)
    users = {user['id_str']: user for user in users}
    tweet_ids = list(set([notice['TweetID'] for notice in notices]))
    tweets = twitter.get_tweets(tweet_ids)
    tweets = {tweet['id_str']: tweet for tweet in tweets}
    get_notice = lambda notice: {
        'Receiver': users.get(notice['ReceiverID']),
        'Sender': users.get(notice['SenderID']),
        'Tweet': tweets.get(notice['TweetID']),
        'Timestamp': notice['Timestamp']
    }
    notices = [get_notice(notice) for notice in notices]
    return notices

# 通知を検索する
def query(receiver_id, size, mode):
    for param in [receiver_id, size]:
        if not param: return []
    params = {
        'IndexName': 'ReceiverID-Timestamp-Index',
        'ProjectionExpression': 'ReceiverID, SenderID, TweetID, #Timestamp',
        'ExpressionAttributeNames': {'#Timestamp': 'Timestamp'},
        'KeyConditionExpression': Key('ReceiverID').eq(receiver_id),
        'ScanIndexForward': False,
        'Limit': size
    }
    response = table.query(**params)
    notices = response['Items']
    while True:
        if len(notices) >= size: break
        if 'LastEvaluatedKey' not in response: break
        params['ExclusiveStartKey'] = response['LastEvaluatedKey']
        params['Limit'] = size - len(notices)
        response = table.query(**params)
        notices = notices + response['Items']
    if mode == 'expand': notices = expand_notices(notices)
    return notices

# 通知を追加/更新する
def put_item(receiver_id, sender_id, tweet_id, timestamp):
    for param in [receiver_id, sender_id, tweet_id, timestamp]:
        if not param: return 'MISSING_PARAMS'
    notice = {
        'ID': f'{receiver_id}-{sender_id}-{tweet_id}',
        'ReceiverID': receiver_id,
        'SenderID': sender_id,
        'TweetID': tweet_id,
        'Timestamp': timestamp
    }
    response = table.put_item(Item = notice)
    status_code = response['ResponseMetadata']['HTTPStatusCode']
    if status_code != 200: return 'INTERNAL_ERROR'
    return 'OK'

# 通知を削除する
def delete_item(receiver_id, sender_id, tweet_id):
    notice = get_item(receiver_id, sender_id, tweet_id)
    if notice is None: return 'NO_DATA_FOUND'
    key = {'ID': f'{receiver_id}-{sender_id}-{tweet_id}'}
    response = table.delete_item(Key = key)
    status_code = response['ResponseMetadata']['HTTPStatusCode']
    if status_code != 200: return 'INTERNAL_ERROR'
    return 'OK'
