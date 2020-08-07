# Twitter-Notice-Manager

Service for managing notifications in Twitter.

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

### Amazon Linux 2 AMI

#### Local

```shell
# Login
$ ssh -i ~/.ssh/example.pem ec2-user@{ELASTIC_IP}
```

#### EC2

```shell
# Update
$ sudo yum update -y

# Install Docker
$ sudo amazon-linux-extras install docker
$ sudo service docker start
$ sudo usermod -a -G docker ec2-user

# Install Docker Compose
$ sudo curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose

# Install Git
$ sudo yum install git

# Deploy
$ git clone https://github.com/KeyTey/Twitter-Notice-Manager.git
$ cd ~/Twitter-Notice-Manager
$ cp .env.example .env
$ $EDITOR .env
$ docker-compose up -d
```
