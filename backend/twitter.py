import os
from requests_oauthlib import OAuth1Session

CK = os.environ['TWITTER_CONSUMER_KEY']
CS = os.environ['TWITTER_CONSUMER_SECRET']
AT = os.environ['TWITTER_ACCESS_TOKEN']
AS = os.environ['TWITTER_ACCESS_SECRET']
session = OAuth1Session(CK, CS, AT, AS)

# ユーザーを取得する
def get_user(user_id = None, screen_name = None):
    url = 'https://api.twitter.com/1.1/users/show.json'
    params = {
        'user_id': user_id,
        'screen_name': screen_name,
        'skip_status': True,
        'include_user_entities': False
    }
    try:
        res = session.get(url, params = params)
    except Exception as error:
        print(error)
        return None
    if res.status_code != 200: return None
    return res.json()

# 複数のユーザーを取得する
def get_users(user_ids = [], screen_names = []):
    url = 'https://api.twitter.com/1.1/users/lookup.json'
    if user_ids != []:
        user_key = 'user_id'
        user_values = user_ids
    else:
        user_key = 'screen_name'
        user_values = screen_names
    params = {
        user_key: ','.join(user_values),
        'skip_status': True,
        'include_user_entities': False
    }
    try:
        res = session.get(url, params = params)
    except Exception as error:
        print(error)
        return []
    if res.status_code != 200: return []
    return res.json()

# 複数のツイートを取得する
def get_tweets(tweet_ids = []):
    url = 'https://api.twitter.com/1.1/statuses/lookup.json'
    params = {
        'id': ','.join(tweet_ids),
        'trim_user': True,
        'include_entities': False
    }
    try:
        res = session.get(url, params = params)
    except Exception as error:
        print(error)
        return []
    if res.status_code != 200: return []
    return res.json()
