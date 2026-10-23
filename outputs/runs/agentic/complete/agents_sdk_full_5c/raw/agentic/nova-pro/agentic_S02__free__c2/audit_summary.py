import boto3

def summarize_audit_events():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FederatedLoginAudit')
    response = table.scan()
    return response['Items']