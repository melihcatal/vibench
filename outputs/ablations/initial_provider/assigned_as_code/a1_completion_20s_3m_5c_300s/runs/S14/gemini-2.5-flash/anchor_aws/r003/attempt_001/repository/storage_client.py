import boto3
import os


def get_s3_client(region_name=None):
    region = region_name or os.environ.get("AWS_REGION")
    if not region:
        raise ValueError("AWS region not specified and not found in environment variables.")
    return boto3.client("s3", region_name=region)
