import os
import boto3

def get_dynamodb_client():
    """
    Provides a configured boto3 DynamoDB client.
    Assumes AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION are set as environment variables.
    """
    return boto3.client(
        "dynamodb",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

def get_dynamodb_resource():
    """
    Provides a configured boto3 DynamoDB resource.
    Assumes AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION are set as environment variables.
    """
    return boto3.resource(
        "dynamodb",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
