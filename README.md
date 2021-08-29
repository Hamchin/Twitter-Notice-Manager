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
| Name | ReceiverID-Timestamp-Index |
| Type | GSI |
| Partition Key | ReceiverID (String) |
| Sort Key | Timestamp (Integer) |

### Items

| Key | Type | Example |
| - | - | - |
| ID | String | 0001-0002-8888 |
| ReceiverID | String | 0001 |
| SenderID | String | 0002 |
| TweetID | String | 8888 |
| Timestamp | Integer | 12345678 |

## Lambda Function

| Attribute | Content |
| - | - |
| Name | TwitterNoticeAPI |
| Runtime | Python 3.8 |
| Memory | 128 MB |
| Timeout | 30 seconds |

### Role

| Attribute | Content |
| - | - |
| Name | LambdaAccess2DynamoDB |
| Policy 1 | AmazonDynamoDBFullAccess |
| Policy 2 | AWSLambdaDynamoDBExecutionRole |

### Environmental Variable

| Key |
| - |
| TWITTER_CONSUMER_KEY |
| TWITTER_CONSUMER_SECRET |
| TWITTER_ACCESS_TOKEN |
| TWITTER_ACCESS_SECRET |

## Lambda Layer

| Attribute | Content |
| - | - |
| Name | OAuthLibrary |
| Runtime | Python 3.8 |

## API Gateway

- Use Lambda Proxy Integration.
- Enable CORS.

### GET /notices

#### Request Parameters

| Key | Type |
| - | - |
| receiver_id <br> (receiver_name) | String |
| size | Integer |
| mode | String |

#### Response Body

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

### POST /notice/update

#### Request Body

| Key | Type |
| - | - |
| receiver_id <br> (receiver_name) | String |
| sender_id <br> (sender_name) | String |
| tweet_id | String |
| timestamp | Integer |

#### Response Body

| Key | Type |
| - | - |
| status | String |

### POST /notice/delete

#### Request Body

| Key | Type |
| - | - |
| receiver_id <br> (receiver_name) | String |
| sender_id <br> (sender_name) | String |
| tweet_id | String |

#### Response Body

| Key | Type |
| - | - |
| status | String |
