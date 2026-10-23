import boto3

from security_client import get_kms_client

def key_usage_summary(key_id):
    kms_client = get_kms_client()
    response = kms_client.describe_key(KeyId=key_id)
    return response['KeyMetadata']