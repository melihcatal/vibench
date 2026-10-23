import boto3


def summarize_audit_events(events):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FederatedLoginAudit')
    for event in events:
        table.put_item(Item=event)
    return 'Audit events summarized'