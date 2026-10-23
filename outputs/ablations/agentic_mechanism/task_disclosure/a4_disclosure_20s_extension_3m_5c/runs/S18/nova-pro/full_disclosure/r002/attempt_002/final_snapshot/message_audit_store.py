import boto3

def store_message_record(message_id, message_data):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('MessageAuditStore')
    table.put_item(
        Item={
            'MessageId': message_id,
            'MessageData': message_data,
            'Timestamp': str(datetime.datetime.now())
        }
    )