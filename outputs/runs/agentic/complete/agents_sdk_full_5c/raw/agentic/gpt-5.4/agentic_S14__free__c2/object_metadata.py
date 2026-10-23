from __future__ import annotations

from typing import Optional

from storage_client import get_s3_client
from storage_models import ObjectMetadata, normalize_head_object


def get_object_metadata(bucket: str, key: str, version_id: Optional[str] = None) -> ObjectMetadata:
    s3 = get_s3_client()
    params = {"Bucket": bucket, "Key": key}
    if version_id:
        params["VersionId"] = version_id
    response = s3.head_object(**params)
    return normalize_head_object(bucket=bucket, key=key, head=response)
