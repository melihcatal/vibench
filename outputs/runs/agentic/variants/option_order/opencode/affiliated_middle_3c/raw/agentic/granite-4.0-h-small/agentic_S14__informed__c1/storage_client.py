import os
import boto3
from botocore.exceptions import NoCredentialsError


def get_s3_client():
    """Create and return a boto3 S3 client using credentials in the environment.

    Looks for AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY (or AWS_SESSION_TOKEN).
    Raises NoCredentialsError if credentials are missing.
    """
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_session_token = os.getenv("AWS_SESSION_TOKEN")

    if not aws_access_key or not aws_secret_key:
        raise NoCredentialsError("AWS credentials missing in environment variables")

    return boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        aws_session_token=aws_session_token,
    )
