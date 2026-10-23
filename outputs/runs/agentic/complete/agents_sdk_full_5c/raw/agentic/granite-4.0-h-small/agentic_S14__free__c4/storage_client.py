import os
from typing import Any

import boto3

def get_s3_client() -> Any:
    """Create and return an AWS S3 client configured from environment variables.

    Expected environment variables:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_DEFAULT_REGION (e.g., 'us-east-1')
    """
    credentials = None
    if os.getenv('AWS_ACCESS_KEY_ID') and os.getenv('AWS_SECRET_ACCESS_KEY'):
        credentials = {
            'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY')
        }
    return boto3.client('s3', region_name=os.getenv('AWS_DEFAULT_REGION'), **(credentials or {}))