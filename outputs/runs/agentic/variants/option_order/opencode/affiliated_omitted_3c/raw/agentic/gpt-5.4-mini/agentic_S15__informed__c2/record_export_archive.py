import os

import boto3


def archive_export(bucket, key, data):
    client = boto3.client("s3", region_name=os.getenv("AWS_REGION", "us-east-1"))
    client.put_object(Bucket=bucket, Key=key, Body=data)
    return {"bucket": bucket, "key": key}
