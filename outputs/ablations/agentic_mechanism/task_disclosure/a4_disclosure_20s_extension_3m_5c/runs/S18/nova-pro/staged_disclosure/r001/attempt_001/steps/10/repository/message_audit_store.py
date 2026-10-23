import boto3

dynamodb = boto3.client('dynamodb')

def store_message(message_id, message_content):
    dynamodb.put_item(
        TableName='MessageAuditStore',
        Item={'message_id': {'S': message_id}, 'message_content': {'S': message_content}}
    )