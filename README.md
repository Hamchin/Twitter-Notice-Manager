# NoticeDB

https://notice-database.herokuapp.com

## Development

### Server 1

```
$ python3 app.py
```

### Server 2

```
$ postgres -D /usr/local/var/postgres
```

### Server 3

```
$ createdb notice
$ python3

>>> from app import db
>>> db.create_all()

$ dropdb notice
```

## Deployment

```
$ heroku create
$ heroku config:set ACCEPTED_IP="<YOUR IP>"
$ heroku config:set TWITTER_CONSUMER_KEY="<YOUR CONSUMER KEY>"
$ heroku config:set TWITTER_CONSUMER_SECRET="<YOUR CONSUMER SECRET>"
$ heroku config:set TWITTER_ACCESS_TOKEN="<YOUR ACCESS TOKEN>"
$ heroku config:set TWITTER_ACCESS_SECRET="<YOUR ACCESS SECRET>"
$ heroku addons:create heroku-postgresql:hobby-dev
$ git push heroku master
$ heroku run python

>>> from app import db
>>> db.create_all()
```
