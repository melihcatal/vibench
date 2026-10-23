import boto3

def get_key_usage_summary():
    client = boto3.client('kms')
    response = client.describe_key(KeyId='alias/myKey')
    return response['KeyMetadata']