import os

import boto3


def metrics_export_archive(bucket: str, key: str, body: bytes):
    client = boto3.client("s3", aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"), region_name=os.getenv("AWS_REGION"))
    return client.put_object(Bucket=bucket, Key=key, Body=body)
