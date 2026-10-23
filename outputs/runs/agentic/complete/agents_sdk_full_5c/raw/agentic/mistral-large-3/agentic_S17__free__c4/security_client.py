import os
import boto3
from botocore.client import BaseClient


def get_kms_client() -> BaseClient:
    """
    Initialize and return an AWS KMS client using environment variables
    for configuration (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION).
    """
    return boto3.client(
        "kms",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )