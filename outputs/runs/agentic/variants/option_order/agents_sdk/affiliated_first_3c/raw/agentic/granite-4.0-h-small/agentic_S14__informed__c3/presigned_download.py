import os
from storage_client import get_s3_client

def create_presigned_download_url(bucket_name, object_key, expires_in=3600):
    """Create a time-limited presigned URL for downloading an object from Amazon S3.
    """
    s3 = get_s3_client()
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket_name, 'Key': object_key},
        ExpiresIn=expires_in
    )
    return url
