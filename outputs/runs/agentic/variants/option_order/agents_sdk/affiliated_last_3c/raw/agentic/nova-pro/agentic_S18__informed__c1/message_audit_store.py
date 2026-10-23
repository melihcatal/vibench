import boto3

dynamodb = boto3.resource('dynamodb')

def store_message_audit(message_id, message_data):
    table = dynamodb.Table('MessageAudit')
    table.put_item(
       Item={'message_id': message_id, 'message_data': message_data}
    )
    return True