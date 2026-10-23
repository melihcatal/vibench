from __future__ import annotations

from typing import Optional

from storage_client import get_s3_client, load_storage_config
from storage_models import SignedUrlResult


def presigned_download(bucket: Optional[str], key: str, expires_in_seconds: int = 900) -> SignedUrlResult:
    client = get_s3_client()
    resolved_bucket = bucket or load_storage_config().bucket
    if not resolved_bucket:
        raise ValueError("bucket is required")

    url = client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": resolved_bucket, "Key": key},
        ExpiresIn=expires_in_seconds,
    )
    return SignedUrlResult(bucket=resolved_bucket, key=key, url=url, expires_in_seconds=expires_in_seconds)
