import boto3
import os

def get_kms_client():
    """
    Provides a configured AWS KMS client.
    """
    return boto3.client(
        "kms",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

