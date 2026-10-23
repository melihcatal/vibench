from __future__ import annotations

from storage_client import get_s3_client
from storage_models import ObjectMetadataResult, normalize_metadata_result


def get_object_metadata(bucket: str, object_name: str) -> ObjectMetadataResult:
    s3 = get_s3_client()
    response = s3.head_object(Bucket=bucket, Key=object_name)
    return normalize_metadata_result(bucket, object_name, response)
