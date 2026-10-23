from __future__ import annotations

from typing import Dict

from storage_client import get_s3_client, load_storage_config
from storage_models import DownloadUrlRequest


def create_presigned_download_url(bucket: str, key: str, expires_in: int = 3600) -> Dict[str, str]:
    config = load_storage_config(bucket)
    client = get_s3_client(config)
    request = DownloadUrlRequest(bucket=bucket, key=key, expires_in=expires_in)
    url = client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": request.bucket, "Key": request.key},
        ExpiresIn=request.expires_in,
    )
    return {"bucket": request.bucket, "key": request.key, "url": url, "expires_in": str(request.expires_in)}
