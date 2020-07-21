# NoticeDB

Service for managing liked notifications in Twitter.

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
$ cp .env.example .env
$ $EDITOR .env
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
