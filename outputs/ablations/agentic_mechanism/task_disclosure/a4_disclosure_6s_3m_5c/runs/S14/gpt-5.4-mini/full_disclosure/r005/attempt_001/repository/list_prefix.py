import os
from typing import Any, Dict, List, Optional

import boto3


def _client():
    return boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.environ.get("AWS_SESSION_TOKEN"),
        region_name=os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"),
    )


def list_prefix(bucket: str, prefix: str = "", delimiter: Optional[str] = None, max_keys: Optional[int] = None) -> Dict[str, Any]:
    params: Dict[str, Any] = {"Bucket": bucket, "Prefix": prefix}
    if delimiter is not None:
        params["Delimiter"] = delimiter
    if max_keys is not None:
        params["MaxKeys"] = max_keys

    response = _client().list_objects_v2(**params)
    contents: List[Dict[str, Any]] = []
    for item in response.get("Contents", []):
        contents.append(
            {
                "key": item.get("Key"),
                "size": item.get("Size"),
                "last_modified": item.get("LastModified").isoformat() if item.get("LastModified") else None,
                "etag": item.get("ETag"),
                "storage_class": item.get("StorageClass"),
            }
        )

    return {
        "bucket": bucket,
        "prefix": prefix,
        "is_truncated": response.get("IsTruncated", False),
        "next_continuation_token": response.get("NextContinuationToken"),
        "keys": contents,
        "common_prefixes": [p.get("Prefix") for p in response.get("CommonPrefixes", [])],
    }


__all__ = ["list_prefix"]
