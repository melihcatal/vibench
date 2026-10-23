from __future__ import annotations

from typing import Optional

from storage_client import get_s3_client, resolve_bucket_name, resolve_key
from storage_models import SignedUrlRequest


def presigned_download_url(
    bucket: Optional[str],
    key: Optional[str],
    expires_in_seconds: int = 900,
) -> str:
    s3 = get_s3_client()
    request = SignedUrlRequest(bucket=resolve_bucket_name(bucket), key=resolve_key(key), expires_in_seconds=expires_in_seconds)
    return s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": request.bucket, "Key": request.key},
        ExpiresIn=request.expires_in_seconds,
    )
