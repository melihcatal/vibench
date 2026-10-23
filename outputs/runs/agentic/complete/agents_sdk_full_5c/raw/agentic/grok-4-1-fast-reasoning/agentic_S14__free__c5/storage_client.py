import os
import boto3
from typing import Optional, Any

def get_s3_client(region: Optional[str] = None) -> Any:
    if region is None:
        region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    return boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=region,
    )

def download_object(client: Any, bucket: str, key: str) -> bytes:
    response = client.get_object(Bucket=bucket, Key=key)
    return response['Body'].read()
