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

$ curl -X POST -H "Content-Type: application/json" -d '{"receive_user": "Taro", "send_user": "Hanako", "tweet_id": "0123456789", "datetime": "2020-01-01T00:00:00.000Z"}' http://0.0.0.0:8080/notice
$ curl -X POST -H "Content-Type: application/json" -d '{"notices": [{"receive_user": "A", "send_user": "B", "tweet_id": "0", "datetime": "0"}, {"receive_user": "C", "send_user": "D", "tweet_id": "0", "datetime": "0"}]}' http://0.0.0.0:8080/notices
$ curl http://0.0.0.0:8080/notices
$ curl -X DELETE http://0.0.0.0:8080/notices
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
