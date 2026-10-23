import boto3

def summarize_key_usage_and_crypto_events():
    cloudtrail_client = boto3.client('cloudtrail')
    events = cloudtrail_client.lookup_events(
       LookupAttributes=[
           {'EventName': 'Encrypt'}, 
           {'EventName': 'Decrypt'},
           {'EventName': 'GenerateDataKey'},
           {'EventName': 'GenerateDataKeyWithoutPlaintext'}
       ]
    )
    event_summary = {
        'Encrypt': 0,
        'Decrypt': 0,
        'GenerateDataKey': 0,
        'GenerateDataKeyWithoutPlaintext': 0
    }
    for event in events['Events']:
        event_name = event['EventName']
        if event_name in event_summary:
            event_summary[event_name] += 1
    return event_summary

if __name__ == '__main__':
    summary = summarize_key_usage_and_crypto_events()
    print(summary)