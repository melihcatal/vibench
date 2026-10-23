import boto3

from storage_client import get_s3_client


def get_object_metadata(object_name, bucket, config=None):
    config = config or {}
    client = get_s3_client(config)
    response = client.head_object(Bucket=bucket, Key=object_name)
    return response