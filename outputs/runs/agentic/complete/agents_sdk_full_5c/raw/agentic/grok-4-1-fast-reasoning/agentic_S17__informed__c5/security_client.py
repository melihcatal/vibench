import os
import boto3
from typing import Optional
from botocore.exceptions import ClientError, NoCredentialsError
from security_models import KeyConfig

def get_kms_client(key_config: Optional[KeyConfig] = None) -> boto3.client:
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    region = key_config.region if key_config else os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    
    if not access_key or not secret_key:
        raise NoCredentialsError("AWS credentials not found in environment variables.")
    
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )
    return session.client('kms')
