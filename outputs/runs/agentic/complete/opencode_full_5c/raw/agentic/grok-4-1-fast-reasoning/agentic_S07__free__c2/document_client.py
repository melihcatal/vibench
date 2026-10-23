import os
import boto3


def get_textract_client(region: str = None) -> boto3.client:
    region = region or os.getenv("AWS_REGION", "us-east-1")
    return boto3.client("textract", region_name=region)
