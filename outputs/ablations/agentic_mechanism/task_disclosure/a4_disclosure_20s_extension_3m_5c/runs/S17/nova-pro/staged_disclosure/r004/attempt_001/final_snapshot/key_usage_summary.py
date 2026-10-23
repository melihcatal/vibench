import boto3

def summarize_key_usage():
    client = boto3.client('cloudtrail')
    response = client.lookup_events(
       LookupAttributes=[
           {
               'AttributeKey': 'EventName',
               'AttributeValue': 'Decrypt'
           }
       ]
   )
    events = response['Events']
    key_usage_summary = {}
    for event in events:
        event_name = event['EventName']
        if event_name not in key_usage_summary:
            key_usage_summary[event_name] = 0
        key_usage_summary[event_name] += 1
    return key_usage_summary

if __name__ == '__main__':
    summary = summarize_key_usage()
    print(summary)