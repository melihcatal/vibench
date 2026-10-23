from __future__ import annotations

from pathlib import Path
from typing import BinaryIO, Optional, Union

from storage_client import get_s3_client, resolve_bucket_name
from storage_models import UploadRequest


def upload_object(
    bucket: Optional[str],
    key: str,
    data: Union[bytes, bytearray, memoryview, BinaryIO, str, Path],
    content_type: Optional[str] = None,
    metadata: Optional[dict[str, str]] = None,
) -> dict:
    s3 = get_s3_client()
    payload: bytes
    if isinstance(data, (bytes, bytearray, memoryview)):
        payload = bytes(data)
    elif hasattr(data, "read"):
        payload = data.read()
        if isinstance(payload, str):
            payload = payload.encode("utf-8")
    else:
        payload = Path(data).expanduser().read_bytes()

    request = UploadRequest(bucket=resolve_bucket_name(bucket), key=key, content=payload, content_type=content_type, metadata=metadata or {})
    extra_args = {"Metadata": request.metadata}
    if request.content_type:
        extra_args["ContentType"] = request.content_type
    response = s3.put_object(Bucket=request.bucket, Key=request.key, Body=request.content, **extra_args)
    return {"bucket": request.bucket, "key": request.key, "etag": response.get("ETag")}
