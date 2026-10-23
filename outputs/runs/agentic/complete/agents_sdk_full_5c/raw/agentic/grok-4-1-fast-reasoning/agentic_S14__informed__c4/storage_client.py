import os
from typing import Any

def get_s3_client() -> Any:
    import boto3
    return boto3.client('s3')

def get_storage_bucket() -> str:
    bucket = os.getenv('STORAGE_BUCKET')
    if not bucket:
        raise ValueError('STORAGE_BUCKET environment variable not set')
    return bucket