import boto3
import os


def get_kms_client():
    """
    Initializes and returns a Boto3 KMS client.
    Expects AWS credentials and region to be configured in the environment.
    """
    return boto3.client(
        "kms",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )
