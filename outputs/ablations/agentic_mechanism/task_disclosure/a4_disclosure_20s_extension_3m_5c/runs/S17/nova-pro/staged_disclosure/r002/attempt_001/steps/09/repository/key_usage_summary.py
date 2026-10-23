import boto3

def summarize_key_usage():
    cloudtrail = boto3.client('cloudtrail')
    response = cloudtrail.lookup_events(
       LookupAttributes=[
           {
               'AttributeKey': 'EventName',
               'AttributeValue': 'Encrypt'
           },
       ],
       MaxResults=50
   )
    key_usage_summary = {
        'total_events': len(response['Events']),
        'event_details': []
    }
    for event in response['Events']:
        key_usage_summary['event_details'].append({
            'event_time': event['EventTime'],
            'event_name': event['EventName'],
            'resources': event['Resources']
        })
    return key_usage_summary

if __name__ == '__main__':
    summary = summarize_key_usage()
    print(summary)