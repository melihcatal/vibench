import boto3

def message_audit_store(table_name, message):
    dynamodb_client = boto3.client('dynamodb', region_name='us-west-2')
    response = dynamodb_client.put_item(
        TableName=table_name,
        Item={'message_id': {'S': message['message_id']}, 'content': {'S': message['content']}}
    )
    return response