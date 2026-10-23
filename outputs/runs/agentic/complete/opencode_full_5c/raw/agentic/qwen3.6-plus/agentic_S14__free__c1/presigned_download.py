from __future__ import annotations

from typing import Optional

from storage_client import get_s3_client, create_presigned_url as _create_presigned_url
from storage_models import PresignedUrlRequest, PresignedUrlResponse


def create_presigned_download_url(
    bucket: str,
    key: str,
    expiration_seconds: int = 3600,
    client=None,
) -> PresignedUrlResponse:
    if client is None:
        client = get_s3_client()

    request = PresignedUrlRequest(
        bucket=bucket,
        key=key,
        expiration_seconds=expiration_seconds,
        http_method="GET",
    )

    return _create_presigned_url(request, client=client)
