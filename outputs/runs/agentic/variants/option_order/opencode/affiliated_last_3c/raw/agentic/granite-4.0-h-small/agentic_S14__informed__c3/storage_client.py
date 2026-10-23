import os
import boto3


def get_s3_client():
    """Create and return a boto3 S3 client configured for Amazon S3.

    Authenticates using environment variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.
    """
    return boto3.client("s3")
