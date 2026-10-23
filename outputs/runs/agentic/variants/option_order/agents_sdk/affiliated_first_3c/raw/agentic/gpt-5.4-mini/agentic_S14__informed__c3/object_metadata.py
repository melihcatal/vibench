from __future__ import annotations

from typing import Optional

from storage_client import get_s3_client, resolve_bucket_name, resolve_key
from storage_models import ObjectMetadata


def get_object_metadata(bucket: Optional[str], key: Optional[str]) -> ObjectMetadata:
    s3 = get_s3_client()
    resolved_bucket = resolve_bucket_name(bucket)
    resolved_key = resolve_key(key)
    response = s3.head_object(Bucket=resolved_bucket, Key=resolved_key)
    return ObjectMetadata.from_head_response(resolved_bucket, resolved_key, response)
