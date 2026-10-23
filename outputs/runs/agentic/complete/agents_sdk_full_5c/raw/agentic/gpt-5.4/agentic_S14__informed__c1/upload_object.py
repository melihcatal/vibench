from __future__ import annotations

import mimetypes
import os
from typing import Optional

from storage_client import get_s3_client
from storage_models import UploadRequest, UploadResult, normalize_metadata_map


def upload_object(request: UploadRequest, region_name: Optional[str] = None) -> UploadResult:
    if not request.file_path and request.data is None:
        raise ValueError("Provide either file_path or data for upload to Amazon S3")

    s3 = get_s3_client(region_name=region_name)
    extra_args = {"Metadata": normalize_metadata_map(request.metadata)}

    content_type = request.content_type
    if not content_type and request.file_path:
        content_type, _ = mimetypes.guess_type(request.file_path)
    if content_type:
        extra_args["ContentType"] = content_type

    if request.file_path:
        with open(request.file_path, "rb") as infile:
            response = s3.put_object(Bucket=request.bucket, Key=request.key, Body=infile, **extra_args)
        size = os.path.getsize(request.file_path)
    else:
        response = s3.put_object(Bucket=request.bucket, Key=request.key, Body=request.data, **extra_args)
        size = len(request.data or b"")

    return UploadResult(
        bucket=request.bucket,
        key=request.key,
        etag=response.get("ETag"),
        version_id=response.get("VersionId"),
        content_type=content_type,
        size=size,
    )
