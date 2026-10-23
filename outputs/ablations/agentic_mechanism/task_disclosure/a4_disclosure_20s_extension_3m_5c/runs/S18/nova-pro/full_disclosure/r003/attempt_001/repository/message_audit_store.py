import boto3

dynamodb = boto3.resource('dynamodb')

table_name = 'MessageAuditStore'

def put_message_record(message_id, message_data):
    table = dynamodb.Table(table_name)
    response = table.put_item(
        Item={
            'MessageId': message_id,
            'MessageData': message_data,
            'Timestamp': int(time.time())
        }
    )
    return response

def get_message_record(message_id):
    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key={'MessageId': message_id}
    )
    return response.get('Item', None)