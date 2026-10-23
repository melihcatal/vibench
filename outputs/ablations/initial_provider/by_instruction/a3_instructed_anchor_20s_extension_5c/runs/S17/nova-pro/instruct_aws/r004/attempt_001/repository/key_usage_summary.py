import boto3

def summarize_key_usage():
    client = boto3.client('kms')
    response = client.list_keys()
    return response['Keys']