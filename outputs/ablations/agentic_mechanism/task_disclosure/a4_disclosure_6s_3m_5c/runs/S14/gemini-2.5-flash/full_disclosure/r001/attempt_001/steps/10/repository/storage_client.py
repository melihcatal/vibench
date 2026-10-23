import os
import boto3

def get_s3_client():
    """
    Provides a configured boto3 S3 client.
    Assumes AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION_NAME
    are set as environment variables.
    """
    region = os.environ.get("AWS_REGION_NAME", "us-east-1")
    s3_client = boto3.client(
        "s3",
        region_name=region,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    return s3_client
