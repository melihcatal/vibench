import os
import boto3

def get_boto_client():
    """Initializes and returns a boto3 client for Secrets Manager."""
    return boto3.client(
        service_name='secretsmanager',
        region_name=os.environ.get("AWS_REGION"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )
