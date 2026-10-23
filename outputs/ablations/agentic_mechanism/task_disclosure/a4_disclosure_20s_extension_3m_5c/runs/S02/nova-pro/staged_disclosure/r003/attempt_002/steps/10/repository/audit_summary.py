import boto3

def summarize_audit_events():
    cloudtrail_client = boto3.client('cloudtrail')
    response = cloudtrail_client.lookup_events(
       LookupAttributes=[
           {'EventName': 'AssumeRole'},
           {'EventSource': 'sts.amazonaws.com'}
       ]
    )
    audit_events = response['Events']
    summary = {}
    for event in audit_events:
        user_identity = event['Username']
        event_time = event['EventTime']
        if user_identity not in summary:
            summary[user_identity] = []
        summary[user_identity].append(event_time.strftime('%Y-%m-%d %H:%M:%S'))
    return summary

if __name__ == '__main__':
    summary = summarize_audit_events()
    for user, events in summary.items():
        print(f'User: {user}')
        for event in events:
            print(f'  Event Time: {event}')
