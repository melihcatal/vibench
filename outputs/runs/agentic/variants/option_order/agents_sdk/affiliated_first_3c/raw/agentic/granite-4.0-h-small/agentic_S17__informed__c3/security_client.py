import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError

def _make_kms_client():
    """Create and cache an AWS KMS client."""
    return boto3.client(
        'kms',
        region_name=os.getenv('KMS_REGION', 'us-east-1'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )

kms_client = _make_kms_client()
