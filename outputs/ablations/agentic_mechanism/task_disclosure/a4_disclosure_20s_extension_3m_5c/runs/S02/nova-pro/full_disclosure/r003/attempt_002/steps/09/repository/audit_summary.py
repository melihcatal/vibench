import boto3

def summarize_audit_events():
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.scan(TableName='FederatedLoginAudit')
    events = response['Items']
    summary = {}
    for event in events:
        event_type = event['eventType']['S']
        if event_type not in summary:
            summary[event_type] = 0
        summary[event_type] += 1
    return summary

if __name__ == '__main__':
    audit_summary = summarize_audit_events()
    print(audit_summary)