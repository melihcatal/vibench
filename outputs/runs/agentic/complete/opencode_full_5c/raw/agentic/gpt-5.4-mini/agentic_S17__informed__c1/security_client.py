import os
import boto3


def require_region(region=None):
    return region or os.environ.get('AWS_REGION') or os.environ.get('AWS_DEFAULT_REGION') or 'us-east-1'


def get_kms_client(region=None):
    return boto3.client('kms', region_name=require_region(region))


def resolve_key_id(key_id=None):
    return key_id or os.environ.get('KMS_KEY_ID') or os.environ.get('AWS_KMS_KEY_ID')
