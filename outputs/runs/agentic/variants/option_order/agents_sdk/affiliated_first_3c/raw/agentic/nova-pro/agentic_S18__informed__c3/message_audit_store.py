import os
import boto3

os.environ['AWS_ACCESS_KEY_ID'] = 'your_access_key_id'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'your_secret_access_key'

def store_message(message):
    client = boto3.client('dynamodb', region_name='us-west-2')
    client.put_item(
        TableName='MessageAudit',
        Item={'MessageId': {'S': 'unique_id'}, 'Message': {'S': message}}
    )