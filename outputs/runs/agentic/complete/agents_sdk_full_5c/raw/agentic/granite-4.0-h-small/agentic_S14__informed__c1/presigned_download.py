import boto3
from typing import Optional

from .storage_client import get_s3_client

s3 = get_s3_client()

def presigned_download_url(bucket: str, key: str, expires_in: int = 3600) -> Optional[str]:
    """Create a time‑limited presigned URL allowing GET access to the object."""
    try:
        url = s3.s3.generate_presigned_url('get_object',
                                           Params={'Bucket': bucket, 'Key': key},
                                           ExpiresIn=expires_in)
        return url
    except Exception as e:
        raise RuntimeError(f'Failed to generate presigned URL: {e}')
