from __future__ import annotations

from typing import Optional

from storage_client import get_s3_client, resolve_bucket
from storage_models import PresignedDownloadRequest


def presigned_download_url(bucket: Optional[str], key: str, expires_in: int = 3600) -> str:
    request = PresignedDownloadRequest(bucket=resolve_bucket(bucket), key=key, expires_in=expires_in)
    client = get_s3_client()
    return client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": request.bucket, "Key": request.key},
        ExpiresIn=request.expires_in,
    )
