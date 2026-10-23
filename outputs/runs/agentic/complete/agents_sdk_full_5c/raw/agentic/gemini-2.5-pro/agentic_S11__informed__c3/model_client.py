import os
import boto3
from botocore.config import Config

def get_bedrock_client():
    """
    Initializes and returns a Boto3 client for Amazon Bedrock Runtime.
    Reads credentials and region from environment variables.
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION_NAME", "us-east-1")

    if not all([aws_access_key_id, aws_secret_access_key]):
        raise ValueError(
            "AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) are not set."
        )

    retry_config = Config(
        region_name=aws_region,
        retries={
            "max_attempts": 10,
            "mode": "standard",
        },
    )

    client = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        config=retry_config,
    )
    return client

def get_bedrock_metadata_client():
    """
    Initializes and returns a Boto3 client for Amazon Bedrock (for metadata).
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION_NAME", "us-east-1")

    if not all([aws_access_key_id, aws_secret_access_key]):
        raise ValueError(
            "AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) are not set."
        )
    
    config = Config(region_name=aws_region)
    
    client = boto3.client(
        "bedrock",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        config=config,
    )
    return client
