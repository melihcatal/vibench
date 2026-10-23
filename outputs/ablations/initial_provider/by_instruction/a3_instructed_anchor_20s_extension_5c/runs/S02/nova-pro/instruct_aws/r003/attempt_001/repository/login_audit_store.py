import boto3

def store_audit_record(record):
    client = boto3.client('dynamodb')
    client.put_item(
        TableName='AuditRecords',
        Item=record
    )