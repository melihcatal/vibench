from __future__ import annotations

from typing import Any, BinaryIO, Optional, Union

from storage_client import get_s3_client, resolve_bucket
from storage_models import UploadRequest

BodyType = Union[str, bytes, bytearray, BinaryIO]


def upload_object(bucket: Optional[str], key: str, body: BodyType, content_type: Optional[str] = None, metadata: Optional[dict[str, str]] = None, acl: Optional[str] = None) -> dict[str, Any]:
    request = UploadRequest(
        bucket=resolve_bucket(bucket),
        key=key,
        body=body,
        content_type=content_type,
        metadata=metadata or {},
        acl=acl,
    )
    client = get_s3_client()
    extra_args: dict[str, Any] = {}
    if request.content_type:
        extra_args["ContentType"] = request.content_type
    if request.metadata:
        extra_args["Metadata"] = request.metadata
    if request.acl:
        extra_args["ACL"] = request.acl
    if extra_args:
        response = client.put_object(Bucket=request.bucket, Key=request.key, Body=request.body, **extra_args)
    else:
        response = client.put_object(Bucket=request.bucket, Key=request.key, Body=request.body)
    return {"bucket": request.bucket, "key": request.key, "etag": response.get("ETag")}
