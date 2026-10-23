from __future__ import annotations

from typing import List, Optional

from storage_client import create_s3_client, load_storage_config
from storage_models import ListedObject, normalize_s3_list



def list_objects_with_prefix(bucket: str, prefix: str = "", max_keys: int = 1000, continuation_token: Optional[str] = None) -> List[ListedObject]:
    client = create_s3_client(load_storage_config(bucket))
    params = {
        "Bucket": bucket,
        "Prefix": prefix,
        "MaxKeys": max_keys,
    }
    if continuation_token:
        params["ContinuationToken"] = continuation_token
    response = client.list_objects_v2(**params)
    return normalize_s3_list(response.get("Contents", []))
