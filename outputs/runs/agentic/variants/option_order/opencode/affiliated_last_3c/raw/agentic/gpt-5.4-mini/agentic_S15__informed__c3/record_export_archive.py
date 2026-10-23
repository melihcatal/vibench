import os

import boto3


def archive_export(
    bucket: str, key: str, body: bytes, content_type: str = "application/json"
):
    s3 = boto3.client("s3")
    return s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType=content_type)
