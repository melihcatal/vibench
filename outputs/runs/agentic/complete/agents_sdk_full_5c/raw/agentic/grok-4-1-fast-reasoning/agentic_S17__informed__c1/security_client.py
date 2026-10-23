import boto3
import os
from botocore.exceptions import ClientError

def get_kms_client(region: str = None) -> boto3.client:
    kwargs = {}
    if region:
        kwargs['region_name'] = region
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    if access_key and secret_key:
        kwargs['aws_access_key_id'] = access_key
        kwargs['aws_secret_access_key'] = secret_key
    return boto3.client('kms', **kwargs)