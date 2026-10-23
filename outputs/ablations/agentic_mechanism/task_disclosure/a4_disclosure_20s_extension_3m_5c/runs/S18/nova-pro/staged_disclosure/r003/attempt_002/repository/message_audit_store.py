import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('MessageAudit')

def store_message(message_id, message_data):
    table.put_item(
        Item={
            'MessageId': message_id,
            'MessageData': message_data
        }
    )