from datetime import timedelta
from typing import Optional

from storage_client import get_s3_client, resolve_bucket_name, resolve_object_key
from storage_models import PresignedUrlRequest, PresignedUrlResponse


def create_presigned_download_url(request: PresignedUrlRequest) -> PresignedUrlResponse:
    client = get_s3_client()
    bucket = resolve_bucket_name(request.bucket)
    key = resolve_object_key(request.key)
    expires_in = int(request.expires_in_seconds or 3600)
    url = client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires_in,
    )
    return PresignedUrlResponse(bucket=bucket, key=key, url=url, expires_in_seconds=expires_in)
