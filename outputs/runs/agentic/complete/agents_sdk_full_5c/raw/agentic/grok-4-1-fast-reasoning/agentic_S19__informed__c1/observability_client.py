import os
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from typing import Optional

def get_cloudwatch_client(region: Optional[str] = None) -> boto3.client:
    """
    Get boto3 CloudWatch client.
    """
    region = region or os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    session = boto3.Session(region_name=region)
    return session.client('cloudwatch')
