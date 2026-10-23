import os
from storage_client import get_s3_client
from storage_models import PresignedUrlResponse

def create_presigned_download_url(bucket_name: str, object_key: str, expiration: int = 3600) -> PresignedUrlResponse:
    s3_client = get_s3_client()
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': object_key},
        ExpiresIn=expiration
    )
    return PresignedUrlResponse(url=url)
