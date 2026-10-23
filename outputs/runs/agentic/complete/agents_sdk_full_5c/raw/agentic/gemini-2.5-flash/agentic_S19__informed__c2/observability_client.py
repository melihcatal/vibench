import boto3
import os

def get_cloudwatch_client():
    """
    Returns a configured boto3 CloudWatch client.
    Assumes AWS credentials are configured via environment variables
    (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) or AWS config files.
    """
    return boto3.client('cloudwatch', region_name=os.getenv('AWS_REGION', 'us-east-1'))
