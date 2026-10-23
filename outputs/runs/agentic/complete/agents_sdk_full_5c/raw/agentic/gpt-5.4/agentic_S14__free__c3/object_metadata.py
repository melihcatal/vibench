from __future__ import annotations

from typing import Optional

from storage_client import create_s3_client, load_storage_config
from storage_models import ObjectMetadataResult, normalize_s3_metadata



def get_object_metadata(bucket: str, key: str, version_id: Optional[str] = None) -> ObjectMetadataResult:
    client = create_s3_client(load_storage_config(bucket))
    params = {"Bucket": bucket, "Key": key}
    if version_id:
        params["VersionId"] = version_id
    response = client.head_object(**params)
    response["Bucket"] = bucket
    response["Key"] = key
    return normalize_s3_metadata(response)
