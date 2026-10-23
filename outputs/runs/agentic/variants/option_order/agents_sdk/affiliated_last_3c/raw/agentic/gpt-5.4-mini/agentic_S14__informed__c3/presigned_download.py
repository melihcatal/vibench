from __future__ import annotations

from datetime import timedelta

from storage_client import get_bucket_name, get_s3_client


def presigned_download(bucket: str, key: str, expires_in: int = 900) -> str:
    s3 = get_s3_client()
    return s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": get_bucket_name(bucket), "Key": key},
        ExpiresIn=max(1, int(timedelta(seconds=expires_in).total_seconds())),
    )
