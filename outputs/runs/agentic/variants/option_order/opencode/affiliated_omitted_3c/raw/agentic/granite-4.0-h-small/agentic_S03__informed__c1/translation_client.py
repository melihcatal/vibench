import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError


def get_translation_client() -> boto3.client:
    """Create and return an Amazon Translate client.

    Reads AWS credentials from environment variables:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_REGION (optional)
    """
    region = os.getenv("AWS_REGION", "us-east-1")
    try:
        client = boto3.client(
            "translate",
            region_name=region,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Failed to initialize Amazon Translate client: {e}")
    return client
