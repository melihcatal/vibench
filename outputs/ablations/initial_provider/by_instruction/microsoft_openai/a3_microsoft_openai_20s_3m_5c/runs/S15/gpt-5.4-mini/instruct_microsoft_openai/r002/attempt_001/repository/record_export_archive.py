import os

import boto3


def record_export_archive(bucket, key, body):
    s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION", "us-east-1"))
    return s3.put_object(Bucket=bucket, Key=key, Body=body if isinstance(body, (bytes, bytearray)) else str(body).encode())
