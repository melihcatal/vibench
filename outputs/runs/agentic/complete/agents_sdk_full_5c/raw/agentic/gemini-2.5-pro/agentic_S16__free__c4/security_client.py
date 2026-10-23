import os
import boto3

def get_aws_client(service_name: str):
    """
    Creates and returns an AWS boto3 client.
    
    This helper centralizes client creation. Configuration could be
    extended here (e.g., to use specific profiles or credentials).

    Args:
        service_name (str): The name of the AWS service (e.g., 's3', 'secretsmanager').

    Returns:
        A boto3 client instance.
    """
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    
    client = boto3.client(
        service_name,
        region_name=aws_region
    )
    return client

