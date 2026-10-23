import boto3
import os

def get_polly_client():
    region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("polly", region_name=region)
