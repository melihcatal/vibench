import boto3
from storage_client import get_s3_client


def list_objects_with_prefix(bucket: str, prefix: str) -> list[str]:
    client = get_s3_client()
    keys = []
    paginator = client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            keys.append(obj["Key"])
    return keys
