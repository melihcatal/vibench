from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

from storage_client import get_bucket_name, get_s3_client
from storage_models import UploadResult, normalize_metadata


def upload_object(
    key: str,
    data: bytes | BinaryIO | str | Path,
    content_type: str | None = None,
    metadata: dict | None = None,
) -> UploadResult:
    client = get_s3_client()
    bucket = get_bucket_name()
    extra_args = {"Metadata": normalize_metadata(metadata)} if metadata else {}
    if content_type:
        extra_args["ContentType"] = content_type
    if isinstance(data, (str, Path)):
        client.upload_file(str(data), bucket, key, ExtraArgs=extra_args or None)
    else:
        body = data.read() if hasattr(data, "read") else data
        client.put_object(Bucket=bucket, Key=key, Body=body, **extra_args)
    head = client.head_object(Bucket=bucket, Key=key)
    return UploadResult(
        bucket=bucket, key=key, etag=head.get("ETag"), version_id=head.get("VersionId")
    )
