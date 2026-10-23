# storage_client.py
# [HELPER] Managed Object Storage client helper utilities

# Example using Amazon S3 (boto3)
import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Load credentials from environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


def create_s3_client():
    """Creates and returns an S3 client configured with the provided credentials.
    Returns:
        boto3.client: Configured S3 client.
    """
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION,
        )
        return s3
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise RuntimeError("AWS credentials are missing or incomplete.") from e
