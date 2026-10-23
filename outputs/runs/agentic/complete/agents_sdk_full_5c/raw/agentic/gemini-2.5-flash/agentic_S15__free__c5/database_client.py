import boto3
import os

def get_dynamodb_client():
    """
    Provides a configured boto3 DynamoDB client.
    Assumes AWS credentials and region are configured via environment variables
    or ~/.aws/credentials and ~/.aws/config.
    """
    # AWS_REGION environment variable is typically used, e.g., us-east-1
    region_name = os.environ.get('AWS_REGION', 'us-east-1')
    return boto3.client('dynamodb', region_name=region_name)

def get_s3_client():
    """
    Provides a configured boto3 S3 client.
    """
    region_name = os.environ.get('AWS_REGION', 'us-east-1')
    return boto3.client('s3', region_name=region_name)

def get_comprehend_client():
    """
    Provides a configured boto3 Comprehend client.
    """
    region_name = os.environ.get('AWS_REGION', 'us-east-1')
    return boto3.client('comprehend', region_name=region_name)

def get_translate_client():
    """
    Provides a configured boto3 Translate client.
    """
    region_name = os.environ.get('AWS_REGION', 'us-east-1')
    return boto3.client('translate', region_name=region_name)
