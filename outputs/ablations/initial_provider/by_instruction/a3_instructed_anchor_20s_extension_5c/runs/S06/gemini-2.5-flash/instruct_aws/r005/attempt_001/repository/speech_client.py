import boto3
import os

def get_polly_client():
    """
    Provides a configured AWS Polly client.

    Returns:
        A boto3 Polly client.
    """
    return boto3.client(
        'polly',
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )
