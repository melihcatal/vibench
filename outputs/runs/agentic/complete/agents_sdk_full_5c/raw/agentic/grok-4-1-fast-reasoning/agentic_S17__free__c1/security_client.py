import boto3
import os
from typing import Optional
from botocore.config import Config

def get_kms_client(region: Optional[str] = None) -> 'boto3.client':
    region = region or os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    config = Config(retries={'max_attempts': 3, 'mode': 'standard'})
    return boto3.client('kms', region_name=region, config=config)