from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

from storage_client import compact_kwargs, require_bucket, s3_client
from storage_models import UploadRequest, UploadResult


S3_PROVIDER = "Amazon S3"


def upload_object(request: UploadRequest) -> UploadResult:
    client = s3_client()
    bucket = require_bucket(request.bucket)
    extra = compact_kwargs(ContentType=request.content_type, Metadata=request.metadata or None)

    if isinstance(request.data, bytes):
        response = client.put_object(Bucket=bucket, Key=request.key, Body=request.data, **extra)
    elif hasattr(request.data, "read"):
        stream = request.data
        response = client.upload_fileobj(stream, bucket, request.key, ExtraArgs=extra or None)  # type: ignore[arg-type]
        head = client.head_object(Bucket=bucket, Key=request.key)
        return UploadResult(bucket=bucket, key=request.key, etag=head.get("ETag"), version_id=head.get("VersionId"))
    else:
        path = Path(str(request.data))
        with path.open("rb") as fh:
            client.upload_fileobj(fh, bucket, request.key, ExtraArgs=extra or None)  # type: ignore[arg-type]
        head = client.head_object(Bucket=bucket, Key=request.key)
        return UploadResult(bucket=bucket, key=request.key, etag=head.get("ETag"), version_id=head.get("VersionId"))

    return UploadResult(bucket=bucket, key=request.key, etag=response.get("ETag"), version_id=response.get("VersionId"))


def upload_bytes(bucket: str, key: str, data: bytes, content_type: str | None = None, metadata: dict[str, str] | None = None) -> dict:
    request = UploadRequest(bucket=bucket, key=key, data=data, content_type=content_type, metadata=metadata or {})
    return upload_object(request).to_dict()


def upload_file(bucket: str, key: str, file_path: str, content_type: str | None = None, metadata: dict[str, str] | None = None) -> dict:
    request = UploadRequest(bucket=bucket, key=key, data=file_path, content_type=content_type, metadata=metadata or {})
    return upload_object(request).to_dict()
