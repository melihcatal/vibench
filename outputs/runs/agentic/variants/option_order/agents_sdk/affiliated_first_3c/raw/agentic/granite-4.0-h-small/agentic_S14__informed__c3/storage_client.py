import os
import boto3
from botocore.exceptions import NoCredentialsError


def get_s3_client():
    """Create and return a boto3 S3 client configured with environment credentials for Amazon S3.
    Required env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY (and optionally AWS_REGION).
    """
    try:
        return boto3.client('s3')
    except NoCredentialsError:
        raise RuntimeError('AWS credentials not found. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.')
