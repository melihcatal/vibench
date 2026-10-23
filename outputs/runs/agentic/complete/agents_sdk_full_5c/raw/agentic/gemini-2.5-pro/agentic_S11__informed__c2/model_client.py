import os
import boto3

def get_bedrock_client():
    """
    Returns a boto3 client for Amazon Bedrock.
    """
    return boto3.client(
        service_name="bedrock",
        region_name=os.environ.get("AWS_REGION_NAME", "us-east-1"),
    )

def get_bedrock_runtime_client():
    """
    Returns a boto3 client for Amazon Bedrock Runtime.
    """
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=os.environ.get("AWS_REGION_NAME", "us-east-1"),
    )
