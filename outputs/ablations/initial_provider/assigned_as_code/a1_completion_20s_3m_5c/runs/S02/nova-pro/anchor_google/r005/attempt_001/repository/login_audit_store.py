import boto3


def store_audit_record(record):
    client = boto3.client('dynamodb')
    client.put_item(
        TableName='FederatedLoginAudit',
        Item={
            'id': {'S': record['id']},
            'provider_id': {'S': record['provider_id']},
            'timestamp': {'S': record['timestamp']},
            'status': {'S': record['status']}
        }
    )