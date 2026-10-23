import os
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

def get_s3_client():
    """Returns a boto3 S3 client."""
    try:
        # Assumes AWS credentials are configured via environment variables, ~/.aws/config, or IAM roles
        return boto3.client('s3')
    except NoCredentialsError:
        raise ValueError("AWS credentials not available.")