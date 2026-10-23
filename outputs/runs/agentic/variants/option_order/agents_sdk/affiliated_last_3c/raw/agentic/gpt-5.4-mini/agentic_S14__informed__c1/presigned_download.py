from __future__ import annotations

from storage_client import load_config, resolve_key, s3_client


def presigned_download_url(bucket: str, key: str, expires_in: int | None = None) -> str:
    client = s3_client()
    config = load_config()
    return client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": resolve_key(key)},
        ExpiresIn=expires_in or config.presign_expires_in,
    )
