"""Local client helpers for security integrations."""
import os
import boto3

def get_kms_client():
    """
    Initializes and returns a Boto3 client for AWS Key Management Service (KMS).

    Reads configuration from environment variables:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_REGION or AWS_DEFAULT_REGION
    """
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    if not region:
        raise ValueError("AWS region not set. Please set AWS_REGION or AWS_DEFAULT_REGION.")

    return boto3.client(
        "kms",
        region_name=region,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
