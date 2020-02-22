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

$ curl -X POST -H "Content-Type: application/json" -d '{"receive_user": "Taro", "send_user": "Hanako", "tweet_id": "0123456789", "datetime": "2020-01-01T00:00:00.000Z"}' http://0.0.0.0:8080/add
$ curl http://0.0.0.0:8080/get
$ curl -X POST http://0.0.0.0:8080/delete
$ dropdb notice
```

## Deployment

```
$ git push heroku master

// Heroku Dashboard -> Resources -> Add-ons -> Heroku Postgres

$ heroku run python

>>> from app import db
>>> db.create_all()
```
