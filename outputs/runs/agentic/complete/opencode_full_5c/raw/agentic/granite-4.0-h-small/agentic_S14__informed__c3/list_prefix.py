import os

boto3 = __import__("boto3")
from storage_client import ManagedObjectStorageClient


def list_objects_under_prefix(bucket: str, prefix: str, max_keys: int = 1000) -> list:
    """List objects in S3 under a given prefix (simulating folder structure).

    Parameters:
        bucket (str): Bucket name.
        prefix (str): Prefix to filter object keys.
        max_keys (int): Maximum number of keys to return (default 1000).

    Returns:
        list: List of object key strings matching the prefix.
    """
    s3 = ManagedObjectStorageClient(
        service="Amazon S3",
        credentials={
            "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
            "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
        },
    )
    client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    paginator = client.get_paginator("list_objects_v2")
    keys = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        if "Contents" in page:
            keys.extend([obj["Key"] for obj in page["Contents"]])
    return keys
