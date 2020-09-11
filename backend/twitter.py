import os, json
from requests_oauthlib import OAuth1Session

CK = os.environ['TWITTER_CONSUMER_KEY']
CS = os.environ['TWITTER_CONSUMER_SECRET']
AT = os.environ['TWITTER_ACCESS_TOKEN']
AS = os.environ['TWITTER_ACCESS_SECRET']
twitter = OAuth1Session(CK, CS, AT, AS)

# ユーザーを取得する
def get_user(user_id = '', screen_name = ''):
    url = 'https://api.twitter.com/1.1/users/show.json'
    key = 'user_id' if user_id else 'screen_name'
    value = user_id if user_id else screen_name
    params = {key: value, 'include_entities': False}
    try:
        res = twitter.get(url, params = params, timeout = 10)
    except Exception as error:
        print(error)
        return None
    if res.status_code != 200: return None
    return json.loads(res.text)

# 複数のユーザーを取得する
def get_users(user_ids = [], screen_names = []):
    url = 'https://api.twitter.com/1.1/users/lookup.json'
    key = 'user_id' if user_ids != [] else 'screen_name'
    values = user_ids if user_ids != [] else screen_names
    params = {key: ','.join(values), 'include_entities': False}
    try:
        res = twitter.get(url, params = params, timeout = 10)
    except Exception as error:
        print(error)
        return []
    if res.status_code != 200: return []
    return json.loads(res.text)

# 複数のツイートを取得する
def get_tweets(tweet_ids):
    url = 'https://api.twitter.com/1.1/statuses/lookup.json'
    params = {
        'id': ','.join(tweet_ids),
        'include_entities': False,
        'trim_user': True
    }
    try:
        res = twitter.get(url, params = params, timeout = 10)
    except Exception as error:
        print(error)
        return []
    if res.status_code != 200: return []
    return json.loads(res.text)
