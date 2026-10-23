import boto3

def summarize_key_usage():
    cloudtrail_client = boto3.client('cloudtrail')
    response = cloudtrail_client.lookup_events(
       LookupAttributes=[
           {'EventName': 'Encrypt'}, {'EventName': 'Decrypt'}
       ]
    )
    return response['Events']