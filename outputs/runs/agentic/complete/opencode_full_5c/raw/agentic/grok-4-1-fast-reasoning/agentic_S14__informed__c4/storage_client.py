import os
import boto3


def get_aws_client_kwargs() -> dict:
    return {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "region_name": os.getenv("AWS_REGION", "us-east-1"),
    }


def get_s3_client():
    kwargs = get_aws_client_kwargs()
    return boto3.client("s3", **kwargs)
