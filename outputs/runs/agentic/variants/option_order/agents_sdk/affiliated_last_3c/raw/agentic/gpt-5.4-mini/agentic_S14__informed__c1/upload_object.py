from __future__ import annotations

from typing import BinaryIO, Optional, Union

from storage_client import resolve_key, s3_client
from storage_models import UploadResult


def upload_object(bucket: str, key: str, body: Union[bytes, bytearray, BinaryIO], content_type: Optional[str] = None) -> UploadResult:
    client = s3_client()
    object_key = resolve_key(key)
    extra_args = {}
    if content_type:
        extra_args["ContentType"] = content_type
    response = client.put_object(Bucket=bucket, Key=object_key, Body=body, **extra_args)
    return UploadResult(bucket=bucket, key=object_key, etag=response.get("ETag"), version_id=response.get("VersionId"))
