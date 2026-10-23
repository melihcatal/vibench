import os
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from typing import Optional

def get_cloudwatch_client(region_name: Optional[str] = None) -> boto3.client:
    """Get CloudWatch client."""
    if region_name is None:
        region_name = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    try:
        return boto3.client('cloudwatch', region_name=region_name)
    except NoCredentialsError:
        raise ValueError("AWS credentials not found. Set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY or use IAM roles.")