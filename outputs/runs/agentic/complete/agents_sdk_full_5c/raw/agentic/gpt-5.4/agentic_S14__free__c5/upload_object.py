from __future__ import annotations

import base64
import hashlib
import mimetypes
from typing import Optional

from storage_client import get_s3_client, require_bucket
from storage_models import UploadRequest, UploadResult


def upload_object(request: UploadRequest, region_name: Optional[str] = None) -> UploadResult:
    s3 = get_s3_client(region_name)
    bucket = require_bucket(request.bucket)

    extra_args = {}
    if request.content_type:
        extra_args["ContentType"] = request.content_type
    elif request.file_path:
        guessed_type, _ = mimetypes.guess_type(request.file_path)
        if guessed_type:
            extra_args["ContentType"] = guessed_type
    if request.metadata:
        extra_args["Metadata"] = request.metadata

    if request.file_path:
        with open(request.file_path, "rb") as fh:
            body = fh.read()
    elif request.data is not None:
        body = request.data
    else:
        raise ValueError("Either file_path or data must be provided.")

    checksum_sha256 = hashlib.sha256(body).digest()
    extra_args["ChecksumSHA256"] = base64.b64encode(checksum_sha256).decode("ascii")

    response = s3.put_object(Bucket=bucket, Key=request.key, Body=body, **extra_args)
    return UploadResult(
        bucket=bucket,
        key=request.key,
        etag=response.get("ETag"),
        version_id=response.get("VersionId"),
        checksum_sha256=hashlib.sha256(body).hexdigest(),
    )
