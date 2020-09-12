# Twitter-Notice-Manager

https://hamchin.github.io/Twitter-Notice-Manager

Service for managing notifications on Twitter.

## API

| Method | Endpoint | Description |
| - | - | - |
| GET | /notices | Get multiple notifications. |
| POST | /notice/update | Update one notification. |
| POST | /notice/delete | Delete one notification. |

## DynamoDB

| Attribute | Content |
| - | - |
| Table Name | TwitterNotice |
| Capacity Mode | On-Demand |
| Primary Partition Key | ID (String) |

### Index

| Attribute | Content |
| - | - |
| Name | PartitionID-Timestamp-Index |
| Type | GSI |
| Partition Key | PartitionID (Integer) |
| Sort Key | Timestamp (Integer) |

### Items

| Key | Type |
| - | - |
| ID | String |
| ReceiverID | String |
| SenderID | String |
| TweetID | String |
| Timestamp | Integer |
| PartitionID | Integer |

## Lambda Function

| Attribute | Content |
| - | - |
| Name | TwitterNoticeAPI |
| Runtime | Python 3.8 |
| Memory | 128 MB |
| Timeout | 30 seconds |

### Environmental Variable

| Key |
| - |
| TWITTER_CONSUMER_KEY |
| TWITTER_CONSUMER_SECRET |
| TWITTER_ACCESS_TOKEN |
| TWITTER_ACCESS_SECRET |

### Role

| Attribute | Content |
| - | - |
| Name | LambdaAccess2DynamoDB |
| Policy 1 | AmazonDynamoDBFullAccess |
| Policy 2 | AWSLambdaDynamoDBExecutionRole |

To create zip file:

```
$ cd backend
$ zip -r function.zip *.py
```

## Lambda Layer

| Attribute | Content |
| - | - |
| Name | Requests-OAuthlib |
| Runtime | Python 3.8 |

To create zip file:

```
$ cd backend
$ pip3 install -t ./python -r requirements.txt
$ zip -r package.zip ./python
```

## API Gateway

- Use Lambda Proxy Integration.
- Enable CORS.

### /notices - GET

#### Request

| Key | Type |
| - | - |
| size | Integer |
| mode | String |

#### Response

Array of notifications, each of which is:

| Key | Type |
| - | - |
| receiver_id | String |
| sender_id | String |
| tweet_id | String |
| timestamp | Integer |

If `mode` is `expand`:

| Key | Type |
| - | - |
| receiver | User Object |
| sender | User Object |
| tweet | Tweet Object |
| timestamp | Integer |

### /notice/update - POST

#### Request

| Key | Type |
| - | - |
| receiver_id (receiver_name) | String |
| sender_id (sender_name) | String |
| tweet_id | String |
| timestamp | Integer |

#### Response

| Key | Type |
| - | - |
| status | String |

### /notice/delete - POST

#### Request

| Key | Type |
| - | - |
| receiver_id (receiver_name) | String |
| sender_id (sender_name) | String |
| tweet_id | String |

#### Response

| Key | Type |
| - | - |
| status | String |

## GitHub Pages

To deploy:

```
$ git subtree push --prefix frontend origin gh-pages
```
