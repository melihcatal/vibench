import os
import boto3


def get_cloudwatch_client(region: str = None):
    if region is None:
        region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    return boto3.client(
        "cloudwatch",
        region_name=region,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
