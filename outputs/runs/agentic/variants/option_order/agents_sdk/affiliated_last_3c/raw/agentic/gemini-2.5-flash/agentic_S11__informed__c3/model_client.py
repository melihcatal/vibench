import boto3
import os

def get_bedrock_runtime_client():
    """
    Returns a configured boto3 Bedrock Runtime client.
    """
    return boto3.client(
        "bedrock-runtime",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

def get_bedrock_client():
    """
    Returns a configured boto3 Bedrock client (for model listing etc.).
    """
    return boto3.client(
        "bedrock",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
