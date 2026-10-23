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
        if 'Resources' in event:
            for resource in event['Resources']:
                if resource['ResourceType'] == 'AWS::KMS::Key':
                    key_id = resource['ResourceName']
                    if key_id not in key_usage_summary:
                        key_usage_summary[key_id] = 0
                    key_usage_summary[key_id] += 1
    return key_usage_summary

if __name__ == '__main__':
    summary = summarize_key_usage()
    print(summary)