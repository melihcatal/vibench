import os
import boto3

def get_region_name() -> str:
    return os.environ.get('AWS_REGION') or os.environ.get('AWS_DEFAULT_REGION') or 'us-east-1'

def get_kms_key_id() -> str:
    return os.environ.get('AWS_KMS_KEY_ID', 'alias/default-key')

def get_kms_client(region_name: str | None = None):
    return boto3.client('kms', region_name=region_name or get_region_name())
