import os
import boto3

def get_kms_client():
    region_name = os.getenv('AWS_REGION', 'us-west-2')
    return boto3.client('kms', region_name=region_name)

def get_key_id():
    return os.getenv('KMS_KEY_ID', 'arn:aws:kms:us-west-2:123456789012:key/abcdefgh-1234-5678-9012-abcdefghijkl')