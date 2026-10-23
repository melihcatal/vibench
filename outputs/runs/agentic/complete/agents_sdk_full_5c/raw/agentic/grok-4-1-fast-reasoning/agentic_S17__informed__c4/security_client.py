import os
import boto3
from typing import Optional

def get_kms_client(region: Optional[str] = None) -> boto3.client:
    """Get AWS KMS client with config from env."""
    region = region or os.getenv('AWS_REGION', 'us-east-1')
    return boto3.client(
        'kms',
        region_name=region,
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
