import boto3

kms = boto3.client('kms')

def summarize_key_usage():
    response = kms.list_keys()
    return response['Keys']