import boto3


def persist_audit_record(record):
    client = boto3.client('dynamodb')
    client.put_item(
        TableName='FederatedLoginAudit',
        Item={
            'session_id': {'S': record['session_id']},
            'event_time': {'S': record['event_time']},
            'status': {'S': record['status']}
        }
    )