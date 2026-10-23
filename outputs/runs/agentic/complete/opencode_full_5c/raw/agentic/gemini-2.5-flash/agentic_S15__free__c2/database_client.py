import boto3
import os


def get_dynamodb_client():
    """
    Returns a boto3 DynamoDB client.
    Assumes AWS credentials and region are configured via environment variables or AWS config files.
    """
    return boto3.client("dynamodb", region_name=os.getenv("AWS_REGION", "us-east-1"))


def get_comprehend_client():
    """
    Returns a boto3 Comprehend client.
    """
    return boto3.client("comprehend", region_name=os.getenv("AWS_REGION", "us-east-1"))


def get_translate_client():
    """
    Returns a boto3 Translate client.
    """
    return boto3.client("translate", region_name=os.getenv("AWS_REGION", "us-east-1"))


def get_s3_client():
    """
    Returns a boto3 S3 client.
    """
    return boto3.client("s3", region_name=os.getenv("AWS_REGION", "us-east-1"))
