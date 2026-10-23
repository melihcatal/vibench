import os

import boto3


def archive_record_snapshot(data, key):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )
    bucket = os.getenv("S3_BUCKET_NAME")
    s3.put_object(Bucket=bucket, Key=key, Body=data)
    return {"bucket": bucket, "key": key}
