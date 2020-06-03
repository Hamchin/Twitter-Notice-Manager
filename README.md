# NoticeDB

## API

| URI | GET | POST |
| - | :-: | :-: |
| /notices | ○ | × |
| /notice/create | × | ○ |
| /notice/insert | × | ○ |
| /notice/delete/:id | × | ○ |

## Development

```shell
$ pip install -r requirements.txt
$ vim environ.json
$ python3

>>> import app
>>> app.create()

$ python3 app.py
```

## Deployment

```shell
# Create and Start
$ docker-compose up -d

# Stop
$ docker-compose stop

# Start
$ docker-compose start

# Remove
$ docker-compose down (--rmi all)
```
