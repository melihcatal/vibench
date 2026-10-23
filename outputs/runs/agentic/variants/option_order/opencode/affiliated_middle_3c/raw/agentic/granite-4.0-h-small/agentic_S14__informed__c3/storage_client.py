import os
import boto3
from botocore.exceptions import NoCredentialsError


def get_s3_client():
    """Return a boto3 S3 client configured via environment variables.

    Provider: Amazon S3 via boto3 SDK.
    Credentials are read from AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.
    """
    try:
        client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
    except NoCredentialsError:
        raise RuntimeError("AWS credentials not found in environment")
    return client

    print("S3 client configured using AWS credentials from environment")
