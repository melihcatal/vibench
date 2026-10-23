import boto3
from datetime import datetime, timedelta

def summarize_audit_events():
    client = boto3.client('cloudtrail')
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=7)
    
    response = client.lookup_events(
       LookupAttributes=[
           {
               'AttributeKey': 'EventName',
               'AttributeValue': 'AssumeRole'
           }
       ],
      StartTime=start_time,
      EndTime=end_time
    )
    
    audit_events = response['Events']
    summary = {
        'total_events': len(audit_events),
        'events': []
    }
    
    for event in audit_events:
        event_summary = {
            'event_time': event['EventTime'].strftime('%Y-%m-%d %H:%M:%S'),
            'user_identity': event['Username']
        }
        summary['events'].append(event_summary)
    
    return summary

if __name__ == '__main__':
    summary = summarize_audit_events()
    print(summary)