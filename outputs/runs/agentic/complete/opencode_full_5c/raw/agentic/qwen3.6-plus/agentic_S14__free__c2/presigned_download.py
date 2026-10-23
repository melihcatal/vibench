import datetime

from storage_client import get_s3_client, validate_bucket_name, handle_s3_error
from storage_models import PresignedUrlRequest, PresignedUrlResponse


def create_presigned_download_url(
    bucket: str,
    key: str,
    expiration_seconds: int = 3600,
    response_content_disposition: str = None,
    response_content_type: str = None,
    region_name: str = None,
) -> PresignedUrlResponse:
    validate_bucket_name(bucket)
    s3 = get_s3_client(region_name=region_name)
    params = {
        "Bucket": bucket,
        "Key": key,
    }
    if response_content_disposition:
        params["ResponseContentDisposition"] = response_content_disposition
    if response_content_type:
        params["ResponseContentType"] = response_content_type
    try:
        url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params=params,
            ExpiresIn=expiration_seconds,
            HttpMethod="GET",
        )
        expires_at = (
            datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration_seconds)
        ).isoformat() + "Z"
        return PresignedUrlResponse(
            url=url,
            bucket=bucket,
            key=key,
            expires_at=expires_at,
            http_method="GET",
        )
    except Exception as exc:
        handle_s3_error(exc, "generate_presigned_url", bucket, key)


def generate_presigned_urls(
    request: PresignedUrlRequest,
    region_name: str = None,
) -> PresignedUrlResponse:
    return create_presigned_download_url(
        bucket=request.bucket,
        key=request.key,
        expiration_seconds=request.expiration_seconds,
        response_content_disposition=request.response_content_disposition,
        response_content_type=request.response_content_type,
        region_name=region_name,
    )
