import os

import boto3


def metrics_export_archive(bucket, key, body):
    client = boto3.client(
        "s3",
        region_name=os.getenv("AWS_REGION")
        or os.getenv("AWS_DEFAULT_REGION")
        or "us-east-1",
    )
    client.put_object(
        Bucket=bucket or os.getenv("METRICS_EXPORT_BUCKET") or os.getenv("S3_BUCKET"),
        Key=key,
        Body=body,
    )
    return {
        "bucket": bucket
        or os.getenv("METRICS_EXPORT_BUCKET")
        or os.getenv("S3_BUCKET"),
        "key": key,
    }
