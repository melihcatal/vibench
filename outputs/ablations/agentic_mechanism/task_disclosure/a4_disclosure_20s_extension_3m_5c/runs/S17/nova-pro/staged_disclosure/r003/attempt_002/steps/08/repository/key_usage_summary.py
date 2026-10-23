import boto3

def summarize_key_usage_and_crypto_events():
    cloudtrail_client = boto3.client('cloudtrail')
    response = cloudtrail_client.lookup_events(
       LookupAttributes=[
           {
               'AttributeKey': 'EventName',
               'AttributeValue': 'CreateKey'
           },
           {
               'AttributeKey': 'EventName',
               'AttributeValue': 'Encrypt'
           },
           {
               'AttributeKey': 'EventName',
               'AttributeValue': 'Decrypt'
           }
       ]
    )
    key_usage_events = [event for event in response['Events'] if event['EventName'] == 'CreateKey']
    crypto_events = [event for event in response['Events'] if event['EventName'] in ['Encrypt', 'Decrypt']]
    print('Key Usage Events:', key_usage_events)
    print('Crypto Events:', crypto_events)

if __name__ == '__main__':
    summarize_key_usage_and_crypto_events()