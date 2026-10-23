import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError

def get_dynamodb_client():
    """Create and return a reusable DynamoDB client.

    Uses AWS credentials from environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION).
    """
    try:
        region = os.getenv('AWS_REGION', 'us-east-1')
        client = boto3.client('dynamodb', region_name=region)
        return client
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Unable to create DynamoDB client: {e}")