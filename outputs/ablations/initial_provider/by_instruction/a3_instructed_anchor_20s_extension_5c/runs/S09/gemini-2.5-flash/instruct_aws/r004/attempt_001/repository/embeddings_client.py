import boto3
import os

def get_bedrock_client():
    """
    Returns a boto3 client for AWS Bedrock.
    Assumes AWS credentials are configured in the environment or ~/.aws/credentials.
    """
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
