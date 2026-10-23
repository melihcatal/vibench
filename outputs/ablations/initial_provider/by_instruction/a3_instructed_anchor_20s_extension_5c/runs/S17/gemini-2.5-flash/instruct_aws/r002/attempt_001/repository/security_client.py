import os
import boto3

def get_kms_client():
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("kms", region_name=region_name)
