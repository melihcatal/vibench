import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('MessageAudit')


def store_message(message_id, message_content):
    response = table.put_item(
        Item={
            'MessageId': message_id,
            'MessageContent': message_content
        }
    )
    return response


def get_message(message_id):
    response = table.get_item(
        Key={'MessageId': message_id}
    )
    return response.get('Item', None)