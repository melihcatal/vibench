import os
import boto3
from typing import Dict, Any

from storage_client import get_aws_credentials

def create_presigned_download_url(
    bucket: str,
    key: str,
    expiration_seconds: int = 3600
) -> str:
    creds = get_aws_credentials()
    s3_client = boto3.client('s3', **creds)
    
    url = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket,
            'Key': key
        },
        ExpiresIn=expiration_seconds
    )
    return url
