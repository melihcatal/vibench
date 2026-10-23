from __future__ import annotations

import io
from typing import BinaryIO, Optional, Union

from storage_client import get_bucket_name, get_s3_client
from storage_models import UploadResult


def upload_object(
    key: str,
    data: Union[bytes, bytearray, memoryview, BinaryIO],
    content_type: Optional[str] = None,
) -> UploadResult:
    s3 = get_s3_client()
    bucket = get_bucket_name()

    extra_args = {}
    if content_type:
        extra_args["ContentType"] = content_type

    if isinstance(data, (bytes, bytearray, memoryview)):
        body = bytes(data)
    elif isinstance(data, io.BufferedIOBase) or hasattr(data, "read"):
        body = data
    else:
        raise TypeError("data must be bytes-like or a file-like object")

    response = s3.put_object(Bucket=bucket, Key=key, Body=body, **extra_args)
    return UploadResult(bucket=bucket, key=key, etag=response.get("ETag"), version_id=response.get("VersionId"))
