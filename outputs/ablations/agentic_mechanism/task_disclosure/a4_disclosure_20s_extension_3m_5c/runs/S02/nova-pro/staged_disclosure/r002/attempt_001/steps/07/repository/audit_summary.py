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
        'event_names': [event['EventName'] for event in events]
    }
    return summary

if __name__ == '__main__':
    summary = summarize_audit_events()
    print(summary)