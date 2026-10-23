import boto3

def summarize_audit_events():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FederatedLoginAudit')
    response = table.scan()
    events = response['Items']
    event_summary = {}
    for event in events:
        event_type = event['eventType']
        if event_type not in event_summary:
            event_summary[event_type] = 0
        event_summary[event_type] += 1
    return event_summary

if __name__ == '__main__':
    summary = summarize_audit_events()
    print(summary)