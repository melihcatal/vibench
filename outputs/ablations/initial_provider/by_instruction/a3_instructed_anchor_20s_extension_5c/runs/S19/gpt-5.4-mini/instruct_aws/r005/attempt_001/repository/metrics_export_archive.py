import os

import boto3


def metrics_export_archive(bucket: str, key: str, body: str, region_name: str = None):
    s3 = boto3.client("s3", region_name=region_name or os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")))
    s3.put_object(Bucket=bucket, Key=key, Body=body.encode("utf-8"))
    return {"provider": "aws_s3", "bucket": bucket, "key": key}
