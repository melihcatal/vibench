from __future__ import annotations

import base64
import hashlib
import io
import mimetypes
from pathlib import Path
from typing import BinaryIO, Optional, Union

from storage_client import get_s3_client
from storage_models import UploadObjectRequest, UploadObjectResult


BodyType = Union[bytes, bytearray, BinaryIO, str, Path]


def _open_body(body: BodyType) -> tuple[object, Optional[bytes]]:
    if isinstance(body, (bytes, bytearray)):
        raw = bytes(body)
        return io.BytesIO(raw), raw
    if isinstance(body, Path):
        raw = body.read_bytes()
        return io.BytesIO(raw), raw
    if isinstance(body, str):
        path = Path(body)
        raw = path.read_bytes()
        return io.BytesIO(raw), raw
    if hasattr(body, "read"):
        raw = body.read()
        if isinstance(raw, str):
            raw = raw.encode("utf-8")
        return io.BytesIO(raw), raw
    raise TypeError("Unsupported body type for S3 upload")


def upload_object(request: UploadObjectRequest, body: BodyType) -> UploadObjectResult:
    s3 = get_s3_client()
    stream, raw = _open_body(body)
    content_type = request.content_type
    if not content_type:
        guessed, _ = mimetypes.guess_type(request.key)
        content_type = guessed or "application/octet-stream"

    checksum_sha256 = None
    checksum_header = None
    if raw is not None:
        digest = hashlib.sha256(raw).digest()
        checksum_header = base64.b64encode(digest).decode("ascii")
        checksum_sha256 = hashlib.sha256(raw).hexdigest()

    response = s3.put_object(
        Bucket=request.bucket,
        Key=request.key,
        Body=stream,
        ContentType=content_type,
        Metadata=request.metadata,
        StorageClass=request.storage_class or "STANDARD",
        ChecksumSHA256=checksum_header,
    )
    return UploadObjectResult(
        bucket=request.bucket,
        key=request.key,
        etag=response.get("ETag"),
        version_id=response.get("VersionId"),
        checksum_sha256=checksum_sha256,
    )
