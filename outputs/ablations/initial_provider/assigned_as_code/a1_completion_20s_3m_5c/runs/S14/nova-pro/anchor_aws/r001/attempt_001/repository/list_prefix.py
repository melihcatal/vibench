import boto3

from storage_client import get_s3_client


def list_objects_with_prefix(prefix, bucket, config=None):
    config = config or {}
    client = get_s3_client(config)
    response = client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    return response.get('Contents', [])