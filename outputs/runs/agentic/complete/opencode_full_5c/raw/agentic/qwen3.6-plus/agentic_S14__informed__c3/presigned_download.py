import oss2
from datetime import datetime, timedelta
from storage_client import get_oss_bucket, normalize_object_key
from storage_models import PresignedUrlRequest, PresignedUrlResponse


def create_presigned_download_url(
    bucket_name: str,
    object_key: str,
    expires_in_seconds: int = 3600,
) -> PresignedUrlResponse:
    object_key = normalize_object_key(object_key)
    bucket = get_oss_bucket(bucket_name)

    try:
        url = bucket.sign_url("GET", object_key, expires_in_seconds)
        expires_at = datetime.utcnow() + timedelta(seconds=expires_in_seconds)

        return PresignedUrlResponse(
            success=True,
            url=url,
            expires_at=expires_at,
        )
    except oss2.exceptions.OssError as e:
        return PresignedUrlResponse(
            success=False,
            error=str(e),
        )


def generate_presigned_url(request: PresignedUrlRequest) -> PresignedUrlResponse:
    return create_presigned_download_url(
        bucket_name=request.bucket,
        object_key=request.object_key,
        expires_in_seconds=request.expires_in_seconds,
    )
