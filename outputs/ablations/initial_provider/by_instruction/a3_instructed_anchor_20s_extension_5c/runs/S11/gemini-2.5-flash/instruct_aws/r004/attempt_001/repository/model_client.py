import boto3
import os

def get_bedrock_client(service_name: str):
    """
    Provides a boto3 client for AWS Bedrock services.

    Args:
        service_name (str): The name of the AWS service (e.g., "bedrock-runtime", "bedrock").

    Returns:
        boto3.client: An initialized boto3 client.
    """
    region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client(service_name, region_name=region)

def get_bedrock_runtime_client():
    """
    Provides a boto3 client for AWS Bedrock Runtime.
    """
    return get_bedrock_client("bedrock-runtime")

def get_bedrock_meta_client():
    """
    Provides a boto3 client for AWS Bedrock (metadata operations).
    """
    return get_bedrock_client("bedrock")
