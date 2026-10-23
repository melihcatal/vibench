import os
import json
from typing import Optional, Dict, Any

# ---- Configuration ----
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# Minimal S3 client configuration
class S3Config:
    EndpointUrl: Optional[str] = None   # set if using a custom endpoint
    VerifySsl: bool = True
    
    def __init__(self):
        self.endpoint = self.EndpointUrl
        self.verify = self.VerifySsl

# Global configuration singleton
config = S3Config()

# ---- S3 Helper ----
# This module centrally creates boto3 clients using the configured credentials.

def create_s3_client() -> boto3.client:
    """Create and return a configured boto3 S3 client."""
    try:
        client = boto3.client(
            's3',
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            endpoint_url=config.endpoint,
            verify=config.verify
        )
        return client
    except Exception as e:
        raise RuntimeError(f'Unable to configure S3 client: {e}')

# Export a singleton for reuse across same‑scenario files
s3_client = create_s3_client()
# Export higher‑level utilities (mirroring storage_client.py) for convenience in local helpers
def upload_object(bucket: str, key: str, body: bytes, content_type: str = 'application/octet-stream') -> None:
    s3_client.put_object(Bucket=bucket, Key=key, Body=body, ContentType=content_type)

def generate_presigned_url(bucket: str, key: str, expires_in: int = 3600) -> str:
    return s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': key}, ExpiresIn=expires_in)

def head_object(bucket: str, key: str) -> Dict[str, Any]:
    return s3_client.head_object(Bucket=bucket, Key=key)

def list_objects(bucket: str, prefix: str = '', delimiter: str = None, max_keys: int = None):
    paginator = s3_client.get_paginator('list_objects_v2')
    result = paginator.paginate(Bucket=bucket, Prefix=prefix, Delimiter=delimiter, MaxKeys=max_keys)
    contents = []
    prefixes = []
    for page in result:
        contents.extend(page.get('Contents', []))
        prefixes.extend(p.get('Prefix') for p in page.get('CommonPrefixes', []))
    return {'Contents': contents, 'CommonPrefixes': prefixes}
