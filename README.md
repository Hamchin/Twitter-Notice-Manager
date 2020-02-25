# NoticeDB

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
$ heroku create <YOUR APP>
$ heroku config:set TWITTER_CONSUMER_KEY="<YOUR CONSUMER KEY>" --app <YOUR APP>
$ heroku config:set TWITTER_CONSUMER_SECRET="<YOUR CONSUMER SECRET>" --app <YOUR APP>
$ heroku config:set TWITTER_ACCESS_TOKEN="<YOUR ACCESS TOKEN>" --app <YOUR APP>
$ heroku config:set TWITTER_ACCESS_SECRET="<YOUR ACCESS SECRET>" --app <YOUR APP>
$ git push heroku master

// Heroku Dashboard -> Resources -> Add-ons -> Heroku Postgres

$ heroku run python

>>> from app import db
>>> db.create_all()
```
