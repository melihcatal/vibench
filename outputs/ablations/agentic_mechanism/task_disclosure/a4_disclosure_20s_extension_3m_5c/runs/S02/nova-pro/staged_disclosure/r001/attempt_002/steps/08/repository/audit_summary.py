import boto3

def summarize_audit_events():
    client = boto3.client('cloudtrail')
    response = client.lookup_events(
       LookupAttributes=[
           {
               'AttributeKey': 'EventName',
               'AttributeValue': 'FederatedUser'
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
           'event_time': event['EventTime'].strftime('%Y-%m-%d %H:%M:%S'),
           'user_name': event['Username'],
           'event_name': event['EventName']
       }
       summary['event_details'].append(event_detail)
   return summary

if __name__ == '__main__':
    audit_summary = summarize_audit_events()
    print(audit_summary)