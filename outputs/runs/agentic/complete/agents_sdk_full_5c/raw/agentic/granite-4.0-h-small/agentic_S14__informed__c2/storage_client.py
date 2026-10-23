import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def create_aws_s3_client():
    """Create and return a boto3 S3 client using environment credentials."""
    try:
        # boto3 will automatically read AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY from env vars.
        return boto3.client('s3')
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise RuntimeError('AWS credentials not found or incomplete') from e
