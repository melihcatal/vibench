import boto3

def key_usage_summary():
    client = boto3.client('kms')
    response = client.list_keys()
    return response['Keys']