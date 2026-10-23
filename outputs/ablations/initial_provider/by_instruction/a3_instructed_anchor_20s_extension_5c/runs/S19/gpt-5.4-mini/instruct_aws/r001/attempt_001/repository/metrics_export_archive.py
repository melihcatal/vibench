import os

import boto3


def metrics_export_archive(bucket: str, key: str, body: bytes):
    client = boto3.client("s3", region_name=os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1")))
    return client.put_object(Bucket=bucket, Key=key, Body=body)
