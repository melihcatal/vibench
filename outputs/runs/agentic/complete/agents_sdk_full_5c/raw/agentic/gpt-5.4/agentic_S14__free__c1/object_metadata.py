from __future__ import annotations

from typing import Optional

from storage_client import get_default_bucket, get_s3_client
from storage_models import ObjectMetadata, normalize_s3_head


def get_object_metadata(bucket: str, key: str, region: Optional[str] = None) -> ObjectMetadata:
    resolved_bucket = get_default_bucket(bucket)
    s3 = get_s3_client(region=region)
    head = s3.head_object(Bucket=resolved_bucket, Key=key)
    return normalize_s3_head(resolved_bucket, key, head)
