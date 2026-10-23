import boto3
import os

dynamodb = boto3.resource('dynamodb', region_name='us-east-1', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
table = dynamodb.Table('MessageAudit')

def message_audit_store(message):
    table.put_item(Item=message)
    return 'Message stored'