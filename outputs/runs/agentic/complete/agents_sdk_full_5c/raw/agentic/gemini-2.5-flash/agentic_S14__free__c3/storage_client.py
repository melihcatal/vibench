import os
import boto3

# Configure AWS region from environment variable or default
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

def get_s3_client():
    """Returns a Boto3 S3 client."""
    return boto3.client("s3", region_name=AWS_REGION)

def get_textract_client():
    """Returns a Boto3 Textract client."""
    return boto3.client("textract", region_name=AWS_REGION)

def get_translate_client():
    """Returns a Boto3 Translate client."""
    return boto3.client("translate", region_name=AWS_REGION)

def get_bedrock_runtime_client():
    """Returns a Boto3 Bedrock Runtime client for invoking models."""
    return boto3.client("bedrock-runtime", region_name=AWS_REGION)
