import json
import random
import string
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UrlShortenerTable')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    original_url = body.get('originalUrl')

    if not original_url:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'URL is required'})
        }

    short_url_id = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    try:
        table.put_item(
            Item={
                'shortUrlId': short_url_id,
                'originalUrl': original_url,
                'createdAt': int(time.time())
            }
        )
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Could not save URL to DynamoDB: {str(e)}'})
        }

    # Construct the short URL
    short_url = f"https://xyz.execute-api.us-east-1.amazonaws.com/prod/url/{short_url_id}"

    return {
        'statusCode': 200,
        'body': json.dumps({'shortUrl': short_url})
    }