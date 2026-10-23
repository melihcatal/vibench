from datetime import datetime, timezone, timedelta
from typing import Optional
from storage_client import get_s3_client, validate_bucket_name, validate_object_key
from storage_models import PresignedURLRequest, PresignedURLResponse


def create_presigned_download_url(request: PresignedURLRequest) -> PresignedURLResponse:
    if not validate_bucket_name(request.bucket):
        return PresignedURLResponse(
            success=False,
            error_message=f"Invalid bucket name: {request.bucket}",
        )

    if not validate_object_key(request.key):
        return PresignedURLResponse(
            success=False,
            error_message=f"Invalid object key: {request.key}",
        )

    s3_client = get_s3_client()

    params = {
        "Bucket": request.bucket,
        "Key": request.key,
    }

    if request.response_content_disposition:
        params["ResponseContentDisposition"] = request.response_content_disposition

    if request.response_content_type:
        params["ResponseContentType"] = request.response_content_type

    try:
        url = s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params=params,
            HttpMethod=request.http_method,
            ExpiresIn=request.expiration_seconds,
        )

        expires_at = datetime.now(timezone.utc) + timedelta(
            seconds=request.expiration_seconds
        )

        return PresignedURLResponse(
            success=True,
            url=url,
            expires_at=expires_at,
        )
    except Exception as e:
        return PresignedURLResponse(
            success=False,
            error_message=str(e),
        )


def generate_download_url(
    bucket: str,
    key: str,
    expiration_seconds: int = 3600,
    content_disposition: Optional[str] = None,
) -> PresignedURLResponse:
    request = PresignedURLRequest(
        bucket=bucket,
        key=key,
        expiration_seconds=expiration_seconds,
        response_content_disposition=content_disposition,
    )
    return create_presigned_download_url(request)
