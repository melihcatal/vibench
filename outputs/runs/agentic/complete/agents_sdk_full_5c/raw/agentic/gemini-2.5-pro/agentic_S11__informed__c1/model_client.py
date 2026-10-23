import os
import boto3
from typing import Optional

def get_bedrock_client(region_name: Optional[str] = None):
    """
    Initializes and returns a boto3 client for Amazon Bedrock.
    """
    if region_name is None:
        region_name = os.environ.get("AWS_REGION", "us-east-1")

    return boto3.client(
        "bedrock",
        region_name=region_name,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

def get_bedrock_runtime_client(region_name: Optional[str] = None):
    """
    Initializes and returns a boto3 client for the Amazon Bedrock Runtime.
    """
    if region_name is None:
        region_name = os.environ.get("AWS_REGION", "us-east-1")

    return boto3.client(
        "bedrock-runtime",
        region_name=region_name,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
