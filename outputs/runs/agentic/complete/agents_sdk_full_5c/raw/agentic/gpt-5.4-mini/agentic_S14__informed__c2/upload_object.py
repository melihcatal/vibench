from __future__ import annotations

from typing import Any, Dict, Optional, Union

from storage_client import get_s3_client, load_storage_config
from storage_models import UploadRequest, normalize_metadata


def upload_object(
    bucket: str,
    key: str,
    body: Union[bytes, bytearray, str, Any],
    content_type: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    config = load_storage_config(bucket)
    client = get_s3_client(config)
    request = UploadRequest(
        bucket=bucket,
        key=key,
        body=body,
        content_type=content_type,
        metadata=normalize_metadata(metadata),
    )
    extra_args: Dict[str, Any] = {}
    if request.content_type:
        extra_args["ContentType"] = request.content_type
    if request.metadata:
        extra_args["Metadata"] = request.metadata
    response = client.put_object(
        Bucket=request.bucket,
        Key=request.key,
        Body=request.body,
        **extra_args,
    )
    return {
        "bucket": request.bucket,
        "key": request.key,
        "etag": response.get("ETag"),
        "version_id": response.get("VersionId"),
    }
