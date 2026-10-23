import boto3
import os

def get_kms_client():
    """
    Returns an AWS KMS client.
    Assumes AWS credentials are set in environment variables or ~/.aws/credentials.
    """
    region_name = os.environ.get("AWS_REGION_NAME")
    if not region_name:
        raise ValueError("AWS_REGION_NAME environment variable not set.")
    
    # The boto3 library automatically picks up credentials from environment variables
    # (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN)
    # or from ~/.aws/credentials and ~/.aws/config files.
    return boto3.client('kms', region_name=region_name)

def get_cloudwatch_logs_client():
    """
    Returns an AWS CloudWatch Logs client.
    """
    region_name = os.environ.get("AWS_REGION_NAME")
    if not region_name:
        raise ValueError("AWS_REGION_NAME environment variable not set.")
    return boto3.client('logs', region_name=region_name)

def get_comprehend_client():
    """
    Returns an AWS Comprehend client.
    """
    region_name = os.environ.get("AWS_REGION_NAME")
    if not region_name:
        raise ValueError("AWS_REGION_NAME environment variable not set.")
    return boto3.client('comprehend', region_name=region_name)

def get_bedrock_runtime_client():
    """
    Returns an AWS Bedrock Runtime client.
    """
    region_name = os.environ.get("AWS_REGION_NAME")
    if not region_name:
        raise ValueError("AWS_REGION_NAME environment variable not set.")
    return boto3.client('bedrock-runtime', region_name=region_name)

def get_translate_client():
    """
    Returns an AWS Translate client.
    """
    region_name = os.environ.get("AWS_REGION_NAME")
    if not region_name:
        raise ValueError("AWS_REGION_NAME environment variable not set.")
    return boto3.client('translate', region_name=region_name)

