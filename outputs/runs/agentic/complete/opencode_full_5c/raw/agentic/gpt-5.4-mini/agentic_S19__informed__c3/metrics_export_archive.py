import os

import boto3


def metrics_export_archive(bucket, key, body):
    client = boto3.client(
        "s3", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    )
    return client.put_object(Bucket=bucket, Key=key, Body=body)
