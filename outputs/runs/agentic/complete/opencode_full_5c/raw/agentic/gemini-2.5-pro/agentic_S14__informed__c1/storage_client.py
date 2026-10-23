import os
import boto3


def get_storage_client():
    """
    Initializes and returns a Boto3 S3 client.

    Expects AWS credentials and region to be configured in the environment.
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not all([aws_access_key_id, aws_secret_access_key]):
        raise ValueError("AWS credentials are not configured in environment variables.")

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )
    return s3_client
