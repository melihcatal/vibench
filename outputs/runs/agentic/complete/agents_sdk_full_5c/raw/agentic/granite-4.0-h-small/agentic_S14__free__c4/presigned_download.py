import time
import boto3
from storage_client import get_s3_client

def presigned_download_url(bucket_name: str, object_key: str, expiration_seconds: int = 3600):
    """Generate a time-limited presigned URL for downloading an object.

    Uses AWS S3 as the managed object storage provider.
    """
    client = get_s3_client()
    return client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': object_key},
        ExpiresIn=expiration_seconds
    )