# [HELPER] database_client.py

## Amazon DynamoDB example
# Import the DynamoDB client library
import boto3

# Set credentials via environment variables for authentication
# export AWS_ACCESS_KEY_ID="your-access-key-id"
# export AWS_SECRET_ACCESS_KEY="your-secret-access-key"


def get_dynamodb_client():
    """Create and return a DynamoDB client instance.

    Returns:
        boto3.client: Configured DynamoDB client.
    """
    return boto3.client("dynamodb")
