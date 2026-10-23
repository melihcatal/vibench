import os
import boto3


def get_kms_client(region: str = None) -> boto3.client:
    region = region or os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    return boto3.client("kms", region_name=region)
