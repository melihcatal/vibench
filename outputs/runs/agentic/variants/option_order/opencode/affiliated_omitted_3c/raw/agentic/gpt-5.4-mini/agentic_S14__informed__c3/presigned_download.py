from datetime import timedelta
from typing import Optional

from storage_client import get_bucket_name, get_s3_client
from storage_models import PresignedUrlRequest, PresignedUrlResponse


def create_presigned_download_url(object_key: str, expires_in_seconds: int = 3600, bucket: Optional[str] = None) -> PresignedUrlResponse:
    bucket_name = bucket or get_bucket_name()
    client = get_s3_client()
    url = client.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': object_key}, ExpiresIn=expires_in_seconds)
    return PresignedUrlResponse(bucket=bucket_name, key=object_key, url=url, expires_in_seconds=expires_in_seconds)
