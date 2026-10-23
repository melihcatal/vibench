import base64
import hashlib
import mimetypes
import os
from dataclasses import dataclass
from typing import Any, BinaryIO, Dict, Optional, Union

import boto3

@dataclass
class UploadResult:
    bucket: str
    key: str
    etag: Optional[str]
    version_id: Optional[str]
    location: Optional[str]
    extra: Dict[str, Any]


def _client():
    return boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
    )


def _normalize_body(data: Union[str, bytes, bytearray, memoryview, BinaryIO]) -> bytes:
    if hasattr(data, "read"):
        body = data.read()
        return body if isinstance(body, (bytes, bytearray)) else bytes(body)
    if isinstance(data, str):
        return data.encode("utf-8")
    if isinstance(data, (bytearray, memoryview)):
        return bytes(data)
    if isinstance(data, bytes):
        return data
    raise TypeError("Unsupported body type")


def upload_object(
    bucket: str,
    key: str,
    data: Union[str, bytes, bytearray, memoryview, BinaryIO],
    content_type: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
    extra_args: Optional[Dict[str, Any]] = None,
) -> UploadResult:
    body = _normalize_body(data)
    if content_type is None:
        content_type = mimetypes.guess_type(key)[0] or "application/octet-stream"
    args: Dict[str, Any] = {"Bucket": bucket, "Key": key, "Body": body, "ContentType": content_type}
    if metadata:
        args["Metadata"] = metadata
    if extra_args:
        args.update(extra_args)
    response = _client().put_object(**args)
    etag = response.get("ETag")
    version_id = response.get("VersionId")
    location = f"s3://{bucket}/{key}"
    return UploadResult(bucket=bucket, key=key, etag=etag, version_id=version_id, location=location, extra={k: v for k, v in response.items() if k not in {"ETag", "VersionId"}})


def upload_file(
    bucket: str,
    key: str,
    file_path: str,
    metadata: Optional[Dict[str, str]] = None,
    extra_args: Optional[Dict[str, Any]] = None,
) -> UploadResult:
    with open(file_path, "rb") as f:
        return upload_object(bucket=bucket, key=key, data=f, metadata=metadata, extra_args=extra_args)


def content_md5(data: Union[str, bytes, bytearray, memoryview, BinaryIO]) -> str:
    body = _normalize_body(data)
    return base64.b64encode(hashlib.md5(body).digest()).decode("ascii")
