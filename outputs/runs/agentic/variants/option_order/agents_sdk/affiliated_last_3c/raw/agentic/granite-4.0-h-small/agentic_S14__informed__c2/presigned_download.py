import os
from datetime import timedelta
from storage_client import get_s3_client
from storage_models import validate_bucket_and_key

def presigned_download_url(bucket: str, key: str, expires_in: timedelta = timedelta(hours=1)):
    """Generate a time-limited presigned URL for downloading an S3 object.

    bucket: S3 bucket name
    key: object key (path)
    expires_in: duration the URL remains valid (default 1 hour)
    """
    s3 = get_s3_client()
    validate_bucket_and_key(bucket, key)
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=int(expires_in.total_seconds())
    )
    print(f'Presigned download URL for s3://{bucket}/{key}: {url}')
    return url
