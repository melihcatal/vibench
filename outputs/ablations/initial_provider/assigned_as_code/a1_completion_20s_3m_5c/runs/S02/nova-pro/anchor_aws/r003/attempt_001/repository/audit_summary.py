import boto3


def audit_summary(events):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('AuditSummary')
    for event in events:
        table.put_item(Item=event)
    return 'Audit summary updated'