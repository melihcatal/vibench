import os
import boto3
from botocore.client import Config

def get_s3_client():
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region_name = os.environ.get("AWS_REGION_NAME", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) must be set in environment variables.")

    s3_client = boto3.client(
        "s3",
        region_name=aws_region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        config=Config(signature_version="s3v4")
    )
    return s3_client
