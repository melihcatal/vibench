import os
from storage_client import get_s3_client
from storage_models import PresignedUrlResult

def create_presigned_download_url(bucket_name: str, object_key: str, expiration_seconds: int = 3600) -> PresignedUrlResult:
    s3_client = get_s3_client()
    url = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket_name,
            'Key': object_key
        },
        ExpiresIn=expiration_seconds
    )
    return PresignedUrlResult(url=url)
