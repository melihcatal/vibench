import boto3

def login_audit_store(audit_record):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('LoginAudit')
    table.put_item(Item=audit_record)