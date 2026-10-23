import os

import boto3


def record_export_archive(bucket_name: str, object_key: str, data: bytes) -> dict:
    s3 = boto3.client("s3")
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=data)
    return {
        "bucket": bucket_name,
        "key": object_key,
        "archived": True,
        "region": os.getenv("AWS_REGION"),
    }
