import boto3

def summarize_audit_events():
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
        summary['event_details'].append({
            'event_id': event['EventId'],
            'event_name': event['EventName'],
            'event_time': event['EventTime'],
            'resources': event['Resources']
        })
    return summary

if __name__ == '__main__':
    summary = summarize_audit_events()
    print(summary)