import boto3
import os

def get_transcribe_client():
    """Initializes and returns an AWS Transcribe client."""
    region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("transcribe", region_name=region)
