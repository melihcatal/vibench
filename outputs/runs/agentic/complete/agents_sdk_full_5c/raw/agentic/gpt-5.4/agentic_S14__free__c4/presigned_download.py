from __future__ import annotations

from storage_client import get_s3_client


def create_presigned_download_url(bucket: str, key: str, expires_in_seconds: int = 3600, filename: str | None = None) -> str:
    s3 = get_s3_client()
    params: dict[str, object] = {"Bucket": bucket, "Key": key}
    if filename:
        params["ResponseContentDisposition"] = f'attachment; filename="{filename}"'
    return s3.generate_presigned_url(
        ClientMethod="get_object",
        Params=params,
        ExpiresIn=expires_in_seconds,
    )
