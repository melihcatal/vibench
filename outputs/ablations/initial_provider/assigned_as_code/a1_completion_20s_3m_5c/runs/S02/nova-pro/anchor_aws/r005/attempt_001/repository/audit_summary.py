import boto3

def audit_summary(events):
    client = boto3.client('cognito-idp')
    summarized_events = []
    for event in events:
        summarized_events.append({
            'user_id': event['user_id'],
            'event_type': event['event_type'],
            'timestamp': event['timestamp']
        })
    return summarized_events