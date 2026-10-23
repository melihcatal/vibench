from __future__ import annotations

from typing import Optional

from storage_client import create_s3_client, load_storage_config



def create_presigned_download_url(bucket: str, key: str, expires_in: int = 3600, version_id: Optional[str] = None) -> str:
    client = create_s3_client(load_storage_config(bucket))
    params = {"Bucket": bucket, "Key": key}
    if version_id:
        params["VersionId"] = version_id
    return client.generate_presigned_url(
        ClientMethod="get_object",
        Params=params,
        ExpiresIn=expires_in,
    )
