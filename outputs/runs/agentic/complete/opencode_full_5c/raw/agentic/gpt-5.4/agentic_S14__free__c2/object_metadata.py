from __future__ import annotations

from storage_client import build_s3_client, require_bucket
from storage_models import ObjectMetadataResult, normalize_s3_head


def get_object_metadata(bucket: str, key: str) -> ObjectMetadataResult:
    s3 = build_s3_client()
    bucket_name = require_bucket(bucket)
    response = s3.head_object(Bucket=bucket_name, Key=key)
    return normalize_s3_head(bucket_name, key, response)
