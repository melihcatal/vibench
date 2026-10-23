from typing import Optional
from storage_client import get_s3_client

def presigned_download(
    bucket: str,
    object_key: str,
    expiration: int = 3600
) -> str:
    """
    Creates a time-limited presigned download URL for an Amazon S3 object.
    """
    client = get_s3_client()
    url = client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': object_key},
        ExpiresIn=expiration
    )
    return url