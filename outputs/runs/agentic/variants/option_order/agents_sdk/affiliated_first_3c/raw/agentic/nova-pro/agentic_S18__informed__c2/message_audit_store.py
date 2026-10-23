import os
import boto3

def store_message_audit(message_id, message_body):
    dynamodb = boto3.resource('dynamodb', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    table = dynamodb.Table('MessageAudit')
    table.put_item(Item={'MessageID': message_id, 'MessageBody': message_body})
    return 'Message stored'