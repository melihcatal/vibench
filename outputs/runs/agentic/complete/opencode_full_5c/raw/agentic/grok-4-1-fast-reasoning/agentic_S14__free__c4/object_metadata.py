import boto3
from storage_client import get_s3_client
from storage_models import normalize_object_metadata, ObjectMetadata


def get_object_metadata(bucket: str, key: str) -> ObjectMetadata:
    client = get_s3_client()
    response = client.head_object(Bucket=bucket, Key=key)
    return normalize_object_metadata(response)
