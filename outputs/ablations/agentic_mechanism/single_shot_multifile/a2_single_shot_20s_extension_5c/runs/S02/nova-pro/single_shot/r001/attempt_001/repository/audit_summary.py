import boto3

def summarize_audit_events():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FederatedLoginAudit')
    response = table.scan()
    events = response['Items']
    summary = {
        'total_events': len(events),
        'events': events
    }
    return summary
