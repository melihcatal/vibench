import boto3
import os


def get_s3_client():
    """
    Creates and configures a boto3 S3 client.
    
    Expects AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    and optionally AWS_REGION to be configured in the environment.
    """
    # Environment variables AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_SESSION_TOKEN
    # are automatically used by boto3 if present.
    s3_client = boto3.client(
        "s3",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )
    return s3_client
