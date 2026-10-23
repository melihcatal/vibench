from __future__ import annotations

from datetime import timedelta

from storage_client import create_s3_client, load_storage_config, normalize_boto_error


def presigned_download(key: str, expires_in: int = 900) -> dict:
    client = create_s3_client()
    bucket = load_storage_config().bucket
    try:
        url = client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=expires_in,
        )
        return {"bucket": bucket, "key": key, "url": url, "expires_in": expires_in}
    except Exception as exc:
        return {"error": normalize_boto_error(exc)}
