import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('MessageAuditStore')


def persist_message(message_id, message_content):
    table.put_item(
        Item={
            'MessageId': message_id,
            'MessageContent': message_content,
            'Timestamp': int(time.time())
        }
    )


def get_message(message_id):
    response = table.get_item(
        Key={'MessageId': message_id}
    )
    return response.get('Item', None)