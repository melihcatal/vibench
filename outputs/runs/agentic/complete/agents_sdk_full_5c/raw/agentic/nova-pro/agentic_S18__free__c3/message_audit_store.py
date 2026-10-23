import boto3

def store_message_audit(message):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('MessageAudit')
    table.put_item(Item={'message_id': message['message_id'], 'content': message['content'], 'timestamp': message['timestamp']})