import boto3
import os

def get_dynamodb_client():
    """
    Provides a boto3 DynamoDB client instance.
    Configured via environment variables or default AWS config.
    """
    region_name = os.getenv("AWS_REGION", "us-east-1")
    return boto3.client("dynamodb", region_name=region_name)

def get_s3_client():
    """
    Provides a boto3 S3 client instance.
    Configured via environment variables or default AWS config.
    """
    region_name = os.getenv("AWS_REGION", "us-east-1")
    return boto3.client("s3", region_name=region_name)
