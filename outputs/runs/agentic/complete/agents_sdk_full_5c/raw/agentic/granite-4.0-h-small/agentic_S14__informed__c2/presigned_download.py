import os
from urllib.parse import urlencode
from storage_client import create_aws_s3_client
from storage_models import S3PresignResult

def presigned_download_url(bucket_name, object_key, expires_in=3600):
    """Create a time-limited presigned URL for downloading an object from S3.

    Uses AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY for auth.
    Returns a S3PresignResult containing the URL (str) and expiration timestamp (int).
    """
    client = create_aws_s3_client()
    response = client.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket_name, 'Key': object_key},
        ExpiresIn=expires_in,
    )
    expiration = response.get('Expires')
    return S3PresignResult(url=response, expiration=expiration)
