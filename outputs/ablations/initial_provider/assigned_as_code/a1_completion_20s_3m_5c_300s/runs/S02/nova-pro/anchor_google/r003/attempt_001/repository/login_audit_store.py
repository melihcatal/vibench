import boto3


def persist_audit_records(records):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FederatedLoginAudit')
    for record in records:
        table.put_item(Item=record)
    return 'Audit records persisted'