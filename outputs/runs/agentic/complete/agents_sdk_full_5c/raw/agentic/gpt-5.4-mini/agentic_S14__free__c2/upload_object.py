from __future__ import annotations

from pathlib import Path
from typing import BinaryIO, Optional, Union

from storage_client import get_s3_client, load_storage_config
from storage_models import UploadResult


BodyType = Union[bytes, bytearray, memoryview, BinaryIO, str, Path]


def upload_object(bucket: Optional[str], key: str, body: BodyType, content_type: Optional[str] = None) -> UploadResult:
    client = get_s3_client()
    resolved_bucket = bucket or load_storage_config().bucket
    if not resolved_bucket:
        raise ValueError("bucket is required")

    if isinstance(body, (str, Path)):
        with open(body, "rb") as f:
            response = client.put_object(Bucket=resolved_bucket, Key=key, Body=f, ContentType=content_type)
    else:
        response = client.put_object(Bucket=resolved_bucket, Key=key, Body=body, ContentType=content_type)

    return UploadResult(
        bucket=resolved_bucket,
        key=key,
        etag=response.get("ETag"),
        version_id=response.get("VersionId"),
    )
