import base64
import hashlib
import mimetypes
import os
from dataclasses import asdict
from pathlib import Path
from typing import Any, BinaryIO, Dict, Optional, Union

import boto3
from botocore.config import Config

from storage_client import get_s3_client, resolve_bucket_name, resolve_object_key
from storage_models import UploadRequest, UploadResponse, normalize_metadata


def _read_body(source: Union[str, bytes, bytearray, BinaryIO, Path]) -> bytes:
    if isinstance(source, (bytes, bytearray)):
        return bytes(source)
    if isinstance(source, Path):
        return source.read_bytes()
    if isinstance(source, str):
        path = Path(source)
        if path.exists() and path.is_file():
            return path.read_bytes()
        return source.encode("utf-8")
    if hasattr(source, "read"):
        data = source.read()
        if isinstance(data, str):
            return data.encode("utf-8")
        return data
    raise TypeError("Unsupported content source")


def upload_object(
    request: UploadRequest,
    content: Union[str, bytes, bytearray, BinaryIO, Path],
) -> UploadResponse:
    client = get_s3_client()
    bucket = resolve_bucket_name(request.bucket)
    key = resolve_object_key(request.key)
    body = _read_body(content)
    metadata = normalize_metadata(request.metadata)
    content_type = request.content_type or mimetypes.guess_type(key)[0] or "application/octet-stream"
    extra_args: Dict[str, Any] = {"ContentType": content_type}
    if metadata:
        extra_args["Metadata"] = metadata
    if request.acl:
        extra_args["ACL"] = request.acl
    if request.cache_control:
        extra_args["CacheControl"] = request.cache_control
    if request.content_disposition:
        extra_args["ContentDisposition"] = request.content_disposition
    if request.content_encoding:
        extra_args["ContentEncoding"] = request.content_encoding
    if request.sse:
        extra_args["ServerSideEncryption"] = request.sse
    if request.sse_kms_key_id:
        extra_args["SSEKMSKeyId"] = request.sse_kms_key_id
    client.put_object(Bucket=bucket, Key=key, Body=body, **extra_args)
    etag = hashlib.md5(body, usedforsecurity=False).hexdigest()
    return UploadResponse(bucket=bucket, key=key, etag=etag, content_length=len(body), metadata=metadata, content_type=content_type)
