import boto3
import os

def get_transcribe_client():
    # AWS Transcribe Client
    # Ensure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are set
    # Or configure AWS CLI with 'aws configure'
    region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("transcribe", region_name=region)
