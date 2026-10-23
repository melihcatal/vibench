import os

import boto3


def record_export_archive(bucket: str, key: str, content: bytes) -> str:
    s3 = boto3.client("s3")
    s3.put_object(Bucket=bucket, Key=key, Body=content)
    return f"s3://{bucket}/{key}"
