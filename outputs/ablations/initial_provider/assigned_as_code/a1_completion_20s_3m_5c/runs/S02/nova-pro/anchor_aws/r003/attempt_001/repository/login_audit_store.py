import boto3


def login_audit_store(audit_records):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('LoginAudit')
    for record in audit_records:
        table.put_item(Item=record)
    return 'Audit records stored'