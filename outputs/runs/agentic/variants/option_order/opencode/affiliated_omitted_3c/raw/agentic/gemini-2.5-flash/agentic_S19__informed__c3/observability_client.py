import boto3
import os


def get_cloudwatch_client():
    """
    Returns a boto3 CloudWatch client.
    Requires AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.
    """
    return boto3.client(
        "cloudwatch",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )


def get_s3_client():
    """
    Returns a boto3 S3 client.
    Requires AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.
    """
    return boto3.client(
        "s3",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
