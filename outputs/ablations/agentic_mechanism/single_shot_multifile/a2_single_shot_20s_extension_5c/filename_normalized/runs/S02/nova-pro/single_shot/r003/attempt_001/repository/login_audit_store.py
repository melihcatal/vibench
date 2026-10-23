import boto3

def store_audit_record(record):
    client = boto3.client('dynamodb')
    response = client.put_item(
        TableName='LoginAudit',
        Item={
            'id': {'S': record['id']},
            'event_time': {'S': record['event_time']},
            'user_id': {'S': record['user_id']},
            'event_type': {'S': record['event_type']}
        }
    )
    return response