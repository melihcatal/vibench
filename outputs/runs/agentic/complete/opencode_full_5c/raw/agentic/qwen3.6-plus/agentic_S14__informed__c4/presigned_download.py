from datetime import datetime, timedelta, timezone
from typing import Optional

from storage_client import get_s3_client, get_bucket_name
from storage_models import PresignedUrlRequest, PresignedUrlResponse


def presigned_download(
    key: str,
    expiration_seconds: int = 3600,
    bucket: Optional[str] = None,
    response_content_disposition: Optional[str] = None,
) -> PresignedUrlResponse:
    if bucket is None:
        bucket = get_bucket_name()

    s3_client = get_s3_client()

    params = {
        "Bucket": bucket,
        "Key": key,
    }

    if response_content_disposition:
        params["ResponseContentDisposition"] = response_content_disposition

    try:
        url = s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params=params,
            ExpiresIn=expiration_seconds,
            HttpMethod="GET",
        )

        expires_at = datetime.now(timezone.utc) + timedelta(seconds=expiration_seconds)

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
