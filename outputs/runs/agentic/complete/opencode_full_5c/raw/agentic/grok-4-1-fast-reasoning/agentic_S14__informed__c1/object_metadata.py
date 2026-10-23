from storage_client import s3_config
from storage_models import parse_object_metadata, ObjectMetadata
import boto3


def get_object_metadata(bucket: str, key: str) -> ObjectMetadata:
    client = boto3.client("s3", **s3_config)
    resp = client.head_object(Bucket=bucket, Key=key)
    return parse_object_metadata(resp)
