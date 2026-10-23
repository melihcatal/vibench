import boto3
import os

def get_bedrock_client(service_name: str = "bedrock-runtime"):
    """Initializes and returns a boto3 client for AWS Bedrock.

    Args:
        service_name (str): The AWS service name (e.g., "bedrock-runtime", "bedrock").

    Returns:
        boto3.client: An initialized boto3 client.
    """
    region = os.environ.get("AWS_REGION", "us-east-1")
    client = boto3.client(
        service_name,
        region_name=region
    )
    return client
