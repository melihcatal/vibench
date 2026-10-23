import os
import boto3
from storage_models import PresignedUrlResult

def presigned_download_url(bucket_name: str, object_key: str, expires_in_seconds: int = 3600) -> PresignedUrlResult:
    """Create a time-limited presigned URL for downloading an S3 object.

    Uses AWS S3 SDK (boto3). Credentials are expected in AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.
    """
    s3 = boto3.client('s3')
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': object_key},
        ExpiresIn=expires_in_seconds
    )
    return PresignedUrlResult(url=url, expires_at=(datetime.utcnow() + timedelta(seconds=expires_in_seconds)))
