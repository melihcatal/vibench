import boto3

def store_message_audit(message):
    dynamodb_client = boto3.client('dynamodb')
    response = dynamodb_client.put_item(
        TableName='MessageAuditTable',
        Item={
            'MessageId': {'S': message.message_id},
            'MessageBody': {'S': message.message_body}
        }
    )
    return response