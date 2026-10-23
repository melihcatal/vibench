from __future__ import annotations

from typing import Optional

from botocore.exceptions import ClientError

from storage_client import get_s3_client, is_not_found_error, require_bucket
from storage_models import ObjectMetadata, normalize_s3_metadata


def get_object_metadata(bucket: str, key: str, version_id: Optional[str] = None, region_name: Optional[str] = None) -> Optional[ObjectMetadata]:
    s3 = get_s3_client(region_name)
    params = {"Bucket": require_bucket(bucket), "Key": key}
    if version_id:
        params["VersionId"] = version_id
    try:
        head = s3.head_object(**params)
    except ClientError as exc:
        if is_not_found_error(exc):
            return None
        raise
    return normalize_s3_metadata(params["Bucket"], key, head)
