from datetime import datetime, timedelta

from storage_client import get_s3_client, validate_bucket_name, validate_object_key
from storage_models import PresignedUrlRequest, PresignedUrlResponse


def create_presigned_download_url(
    bucket: str,
    key: str,
    expires_in: int = 3600,
    http_method: str = "GET",
    response_content_disposition: str = None,
    response_content_type: str = None,
) -> PresignedUrlResponse:
    client = get_s3_client()
    validate_bucket_name(bucket)
    validate_object_key(key)

    params = {
        "Bucket": bucket,
        "Key": key,
    }

    extra_params = {}
    if response_content_disposition:
        extra_params["ResponseContentDisposition"] = response_content_disposition
    if response_content_type:
        extra_params["ResponseContentType"] = response_content_type

    if extra_params:
        params["Params"] = extra_params

    try:
        url = client.generate_presigned_url(
            ClientMethod="get_object",
            Params=params,
            ExpiresIn=expires_in,
            HttpMethod=http_method,
        )

        expires_at = datetime.utcnow() + timedelta(seconds=expires_in)

        return PresignedUrlResponse(
            success=True,
            url=url,
            expires_at=expires_at,
        )

    except Exception as exc:
        return PresignedUrlResponse(
            success=False,
            error=str(exc),
        )


def create_presigned_url_from_request(
    request: PresignedUrlRequest,
) -> PresignedUrlResponse:
    return create_presigned_download_url(
        bucket=request.bucket,
        key=request.key,
        expires_in=request.expires_in,
        http_method=request.http_method,
        response_content_disposition=request.response_content_disposition,
        response_content_type=request.response_content_type,
    )
