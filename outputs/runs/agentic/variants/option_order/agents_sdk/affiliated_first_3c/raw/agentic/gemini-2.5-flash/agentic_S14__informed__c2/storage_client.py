
import boto3
import os

def get_s3_client():
    # AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are typically loaded from environment variables or ~/.aws/credentials
    # AWS_REGION_NAME can also be configured
    return boto3.client('s3')

def get_textract_client():
    return boto3.client('textract')

def get_translate_client():
    return boto3.client('translate')

def get_bedrock_runtime_client():
    # Ensure AWS_REGION_NAME is configured for Bedrock
    return boto3.client('bedrock-runtime')
