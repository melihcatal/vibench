import os
import boto3

def get_dynamodb_client():
    """
    Provides a configured AWS DynamoDB client.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("dynamodb", region_name=region_name)
