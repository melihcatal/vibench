import os
import boto3


def get_s3_client(region: str = None):
    if region is None:
        region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    return boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
        region_name=region,
    )
