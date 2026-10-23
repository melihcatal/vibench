import boto3
from storage_client import get_aws_creds
from storage_models import normalize_metadata

def object_metadata(bucket: str, key: str) -> dict:
    s3 = boto3.client('s3', **get_aws_creds())
    resp = s3.head_object(Bucket=bucket, Key=key)
    return normalize_metadata(resp)