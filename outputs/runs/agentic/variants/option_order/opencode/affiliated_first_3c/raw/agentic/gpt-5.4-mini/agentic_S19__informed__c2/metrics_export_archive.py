import os

import boto3


def metrics_export_archive(bucket, key, body):
    client = boto3.client(
        "s3",
        region_name=os.getenv(
            "AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        ),
    )
    client.put_object(Bucket=bucket, Key=key, Body=body)
    return {"bucket": bucket, "key": key}
