import boto3
import os

def get_dynamodb_client():
    """
    Returns a boto3 DynamoDB client.
    Assumes AWS credentials and region are configured in environment variables
    or AWS config files.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("dynamodb", region_name=region_name)

def get_s3_client():
    """
    Returns a boto3 S3 client.
    Assumes AWS credentials and region are configured in environment variables
    or AWS config files.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("s3", region_name=region_name)

def get_comprehend_client():
    """
    Returns a boto3 Comprehend client.
    Assumes AWS credentials and region are configured in environment variables
    or AWS config files.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("comprehend", region_name=region_name)

def get_translate_client():
    """
    Returns a boto3 Translate client.
    Assumes AWS credentials and region are configured in environment variables
    or AWS config files.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("translate", region_name=region_name)
