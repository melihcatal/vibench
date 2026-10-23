import os
import boto3
from botocore.client import BaseClient


def get_kms_client() -> BaseClient:
    """
    Initializes and returns an AWS KMS client.
    
    Returns:
        A boto3 KMS client.
    """
    return boto3.client(
        "kms",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )