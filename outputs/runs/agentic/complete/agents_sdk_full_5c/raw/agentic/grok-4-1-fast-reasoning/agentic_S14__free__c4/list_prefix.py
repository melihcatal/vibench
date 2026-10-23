import boto3
from storage_client import get_aws_creds
from storage_models import list_object_keys

def list_prefix(bucket: str, prefix: str = '') -> list[str]:
    s3 = boto3.client('s3', **get_aws_creds())
    return list_object_keys(s3, bucket, prefix)