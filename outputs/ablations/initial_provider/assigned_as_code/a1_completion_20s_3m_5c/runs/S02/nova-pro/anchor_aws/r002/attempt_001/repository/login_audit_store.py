import boto3


def persist_audit_records(audit_records):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FederatedLoginAudit')
    with table.batch_writer() as batch:
        for record in audit_records:
            batch.put_item(Item=record)