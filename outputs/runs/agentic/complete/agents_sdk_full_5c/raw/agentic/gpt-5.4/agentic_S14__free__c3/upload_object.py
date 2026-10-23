from __future__ import annotations

import hashlib
import mimetypes
from typing import Optional

from storage_client import create_s3_client, load_storage_config
from storage_models import UploadObjectRequest, UploadObjectResult



def upload_object(request: UploadObjectRequest) -> UploadObjectResult:
    client = create_s3_client(load_storage_config(request.bucket))
    extra_args = {"Metadata": request.metadata}
    if request.content_type:
        extra_args["ContentType"] = request.content_type
    elif request.file_path:
        guessed_type, _ = mimetypes.guess_type(request.file_path)
        if guessed_type:
            extra_args["ContentType"] = guessed_type

    checksum_sha256: Optional[str] = None
    if request.data is not None:
        checksum_sha256 = hashlib.sha256(request.data).hexdigest()
        response = client.put_object(
            Bucket=request.bucket,
            Key=request.key,
            Body=request.data,
            **extra_args,
        )
    elif request.file_path:
        with open(request.file_path, "rb") as fh:
            payload = fh.read()
        checksum_sha256 = hashlib.sha256(payload).hexdigest()
        client.upload_file(request.file_path, request.bucket, request.key, ExtraArgs=extra_args)
        response = client.head_object(Bucket=request.bucket, Key=request.key)
    else:
        raise ValueError("Either file_path or data must be provided")

    return UploadObjectResult(
        bucket=request.bucket,
        key=request.key,
        etag=(response.get("ETag") or "").strip('"') or None,
        version_id=response.get("VersionId"),
        checksum_sha256=checksum_sha256,
    )
