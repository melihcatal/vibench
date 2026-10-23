import boto3

def store_login_audit(audit_record):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FederatedLoginAudit')
    table.put_item(Item=audit_record)