import os
import boto3
from botocore.exceptions import ClientError

def get_storage_client():
    """
    Creates and returns a Boto3 S3 client.

    Configuration is loaded from environment variables:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_REGION
    """
    try:
        s3_client = boto3.client(
            "s3",
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        )
        # Quick check to ensure credentials are valid
        s3_client.list_buckets()
        return s3_client
    except (ClientError, NoCredentialsError) as e:
        print(f"Error creating S3 client: {e}")
        raise

def get_aws_region():
    """Returns the configured AWS region."""
    return os.environ.get("AWS_REGION", "us-east-1")
