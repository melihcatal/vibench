import boto3
import os

def get_s3_client():
    # AWS S3 client configuration
    # Uses environment variables for credentials and region
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN
    # AWS_REGION or AWS_DEFAULT_REGION
    return boto3.client('s3')
