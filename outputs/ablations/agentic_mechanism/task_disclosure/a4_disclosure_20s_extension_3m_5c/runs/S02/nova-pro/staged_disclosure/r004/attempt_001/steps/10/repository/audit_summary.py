import boto3

def summarize_federated_login_events():
    client = boto3.client('cloudtrail')
    response = client.lookup_events(
       LookupAttributes=[
           {
               'AttributeKey': 'EventName',
               'AttributeValue': 'AssumeRole'
           }
       ]
    )
    events = response['Events']
    summary = {
        'total_events': len(events),
        'event_details': []
    }
    for event in events:
        event_detail = {
            'event_id': event['EventId'],
            'event_time': event['EventTime'],
            'user_identity': event['Username']
        }
        summary['event_details'].append(event_detail)
    return summary

if __name__ == '__main__':
    summary = summarize_federated_login_events()
    print(summary)