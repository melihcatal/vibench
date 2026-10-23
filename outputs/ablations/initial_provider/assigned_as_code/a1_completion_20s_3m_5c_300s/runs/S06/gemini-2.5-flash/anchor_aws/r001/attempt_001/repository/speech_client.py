import boto3
import os


def get_polly_client(region_name=None):
    region = region_name or os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("polly", region_name=region)


def get_s3_client(region_name=None):
    region = region_name or os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("s3", region_name=region)
