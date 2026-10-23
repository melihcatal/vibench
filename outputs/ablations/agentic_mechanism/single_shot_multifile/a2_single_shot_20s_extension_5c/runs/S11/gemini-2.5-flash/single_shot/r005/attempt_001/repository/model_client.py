import os
import boto3
from botocore.config import Config

def get_bedrock_runtime_client():
    """Provides a configured boto3 client for AWS Bedrock Runtime."""
    region_name = os.getenv("AWS_REGION", "us-east-1")
    
    # Optional: Configure retries and timeouts
    boto_config = Config(
        region_name=region_name,
        retries={
            'max_attempts': 10,
            'mode': 'standard'
        }
    )

    # Ensure AWS credentials are set up in environment variables or AWS config files
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN
    client = boto3.client("bedrock-runtime", config=boto_config)
    return client
