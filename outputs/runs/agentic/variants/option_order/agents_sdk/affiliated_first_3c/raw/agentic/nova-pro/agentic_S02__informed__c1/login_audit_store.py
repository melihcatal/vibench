import boto3

def store_audit_record(record):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('LoginAudit')
    table.put_item(Item=record)