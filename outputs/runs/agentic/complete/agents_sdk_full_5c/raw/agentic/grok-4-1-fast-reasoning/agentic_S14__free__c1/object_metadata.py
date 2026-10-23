import boto3
from typing import Dict, Any
from storage_client import S3_CONFIG, BUCKET_NAME
from storage_models import parse_metadata, ObjectMetadata

def get_object_metadata(key: str) -> ObjectMetadata:
    client = boto3.client('s3', **S3_CONFIG)
    resp = client.head_object(Bucket=BUCKET_NAME, Key=key)
    return parse_metadata(resp)
