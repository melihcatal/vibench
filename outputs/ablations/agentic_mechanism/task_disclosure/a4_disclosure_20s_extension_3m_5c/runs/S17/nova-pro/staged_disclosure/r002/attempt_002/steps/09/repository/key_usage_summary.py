import boto3

def summarize_key_usage():
    cloudtrail_client = boto3.client('cloudtrail')
    response = cloudtrail_client.lookup_events(
       LookupAttributes=[
            {'EventName': 'Encrypt'}, {'EventName': 'Decrypt'},
            {'EventName': 'GenerateDataKey'}, {'EventName': 'GenerateDataKeyWithoutPlaintext'}
       ]
    )
    key_usage_summary = {}
    for event in response['Events']:
        event_name = event['EventName']
        if event_name not in key_usage_summary:
            key_usage_summary[event_name] = 0
        key_usage_summary[event_name] += 1
    return key_usage_summary

if __name__ == '__main__':
    key_usage = summarize_key_usage()
    print(key_usage)