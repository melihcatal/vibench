import os
from datetime import datetime, timedelta
from storage_client import get_s3_client
from storage_models import normalize_download_params

def presigned_download_url(bucket, key, expires_in_minutes=60):
    """Creates a time-limited presigned URL for downloading an object from Amazon S3.
    Uses boto3 S3 client from storage_client.py.
    """
    params = normalize_download_params(bucket, key)
    s3 = get_s3_client()
    url = s3.generate_presigned_url(
        'get_object',
        Params=params,
        ExpiresIn=expires_in_minutes * 60
    )
    print(f'Presigned download URL for {key} expires in {expires_in_minutes} minutes.')
    return url
