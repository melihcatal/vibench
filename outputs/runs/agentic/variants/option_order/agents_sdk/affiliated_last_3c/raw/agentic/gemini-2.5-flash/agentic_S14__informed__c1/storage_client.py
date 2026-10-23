import boto3
import os

def get_s3_client():
    """Initializes and returns an AWS S3 client."""
    # AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are typically loaded from environment variables or ~/.aws/credentials
    # For this example, we assume they are configured in the environment or by default boto3 mechanisms.
    return boto3.client('s3')

def get_textract_client():
    """Initializes and returns an AWS Textract client."""
    return boto3.client('textract')

def get_translate_client():
    """Initializes and returns an AWS Translate client."""
    return boto3.client('translate')

def get_bedrock_runtime_client():
    """Initializes and returns an AWS Bedrock Runtime client."""
    return boto3.client(service_name='bedrock-runtime', region_name=os.getenv('AWS_REGION', 'us-east-1'))
