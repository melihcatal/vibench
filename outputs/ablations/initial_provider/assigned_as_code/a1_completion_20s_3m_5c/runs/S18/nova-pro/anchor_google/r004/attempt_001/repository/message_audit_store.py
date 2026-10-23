import boto3


def persist_message_record(message_id, payload, status):
    client = boto3.client('dynamodb')
    table_name = 'message-audit-store'
    client.put_item(
        TableName=table_name,
        Item={'message_id': {'S': message_id},
              'payload': {'S': payload},
              'status': {'S': status}}
    )