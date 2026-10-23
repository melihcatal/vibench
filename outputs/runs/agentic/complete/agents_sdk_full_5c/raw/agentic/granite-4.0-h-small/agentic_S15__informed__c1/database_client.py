import os
import boto3
from botocore.exceptions import ClientError

# Managed NoSQL store: Amazon DynamoDB

def get_dynamodb_client() -> boto3.client:
    """Create and return a boto3 DynamoDB client using AWS credentials from env vars."""
    try:
        client = boto3.client(
            'dynamodb',
            region_name=os.getenv('AWS_REGION', 'us-east-1'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
    except ClientError as e:
        raise RuntimeError(f"Failed to initialize DynamoDB client: {e}")
    return client

if __name__ == "__main__":
    # Simple test client creation (remove in production)
    client = get_dynamodb_client()
    print('DynamoDB client ready:', client)
