import os
from typing import Any, Dict, Optional

from storage_client import build_put_kwargs, get_bucket_name, get_s3_client
from storage_models import body_to_bytes, normalize_key, normalize_metadata


def upload_object(
    bucket: Optional[str],
    key: str,
    body: Any,
    content_type: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    client = get_s3_client()
    target_bucket = get_bucket_name(bucket)
    normalized_key = normalize_key(key)
    payload = body_to_bytes(body)
    kwargs = build_put_kwargs(
        content_type=content_type, metadata=normalize_metadata(metadata)
    )
    response = client.put_object(
        Bucket=target_bucket, Key=normalized_key, Body=payload, **kwargs
    )
    return {
        "bucket": target_bucket,
        "key": normalized_key,
        "etag": response.get("ETag"),
        "version_id": response.get("VersionId"),
    }


if __name__ == "__main__":
    import sys

    upload_object(None, sys.argv[1], sys.stdin.buffer.read())
