import boto3

def get_key_usage_summary(key_id):
    kms = boto3.client('kms')
    response = kms.describe_key(KeyId=key_id)
    return response['KeyMetadata']