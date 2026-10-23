import boto3
import os

def get_transcribe_client():
    # It's recommended to configure AWS credentials and region via environment variables
    # or AWS CLI configuration. Boto3 will automatically pick them up.
    # For explicit configuration, you can pass them here:
    # region_name = os.getenv("AWS_REGION", "us-east-1")
    # return boto3.client("transcribe", region_name=region_name)
    return boto3.client("transcribe")
