import boto3
from security_client import get_kms_client

def key_usage_summary():
    kms_client = get_kms_client()
    response = kms_client.list_keys()
    return response['Keys']