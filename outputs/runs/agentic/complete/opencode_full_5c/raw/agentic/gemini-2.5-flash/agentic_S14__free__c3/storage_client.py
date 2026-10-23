import os
import boto3
from botocore.exceptions import ClientError


def get_s3_client():
    """Initializes and returns an AWS S3 client."""
    # AWS_REGION environment variable or default to 'us-east-1'
    region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("s3", region_name=region)


def get_textract_client():
    """Initializes and returns an AWS Textract client."""
    region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("textract", region_name=region)


def get_translate_client():
    """Initializes and returns an AWS Translate client."""
    region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("translate", region_name=region)


def get_comprehend_client():
    """Initializes and returns an AWS Comprehend client."""
    region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("comprehend", region_name=region)
