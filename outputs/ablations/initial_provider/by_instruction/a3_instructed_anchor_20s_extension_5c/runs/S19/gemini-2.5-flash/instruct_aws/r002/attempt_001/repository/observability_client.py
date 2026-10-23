import boto3
import os

def get_cloudwatch_client():
    """
    Provides a configured AWS CloudWatch client.
    """
    region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client('cloudwatch', region_name=region)
