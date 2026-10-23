import os
import boto3

def get_dynamodb_client():
    """
    Provides a configured boto3 DynamoDB client.
    """
    region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("dynamodb", region_name=region)

def get_dynamodb_resource():
    """
    Provides a configured boto3 DynamoDB resource.
    """
    region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.resource("dynamodb", region_name=region)
