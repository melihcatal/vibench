import os
import boto3

def get_security_client(region=None):
    region = region or os.getenv('AWS_REGION')
    return boto3.client('kms', region_name=region)

def get_config(key_id=None):
    key_id = key_id or os.getenv('AWS_KMS_KEY_ID')
    return {'key_id': key_id}
