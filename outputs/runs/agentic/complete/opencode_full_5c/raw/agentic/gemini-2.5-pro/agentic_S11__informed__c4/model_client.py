import os
import boto3


def get_bedrock_client():
    """
    Initializes and returns a Boto3 client for Amazon Bedrock Runtime.
    Assumes AWS credentials are configured in the environment.
    """
    return boto3.client(
        "bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )
