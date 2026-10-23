import boto3
import os

def get_s3_client():
    # AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are typically loaded from environment variables
    # or AWS credentials file by boto3 automatically.
    # Ensure these are configured for authentication.
    return boto3.client('s3')

def get_textract_client():
    return boto3.client('textract')

def get_translate_client():
    return boto3.client('translate')

def get_bedrock_runtime_client():
    return boto3.client(service_name='bedrock-runtime', region_name=os.environ.get('AWS_REGION', 'us-east-1'))
