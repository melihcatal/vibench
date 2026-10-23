import boto3

def persist_audit_record(record):
    client = boto3.client('dynamodb')
    client.put_item(
        TableName='FederatedLoginAudit',
        Item={
            'user_id': {'S': record['user_id']},
            'event_type': {'S': record['event_type']},
            'timestamp': {'S': record['timestamp']}
        }
    )