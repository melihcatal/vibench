from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

from storage_client import load_settings, get_s3_client
from storage_models import UploadRequest, UploadResponse, dataclass_to_dict


def upload_object(request: UploadRequest) -> UploadResponse:
    s3 = get_s3_client()
    body = request.body
    if body is None and request.body_path:
        body = Path(request.body_path).read_bytes()
    if body is None:
        raise ValueError("upload body or body_path is required")

    put_kwargs = {
        "Bucket": request.bucket,
        "Key": request.key,
        "Body": body,
    }
    if request.content_type:
        put_kwargs["ContentType"] = request.content_type
    if request.metadata:
        put_kwargs["Metadata"] = request.metadata

    response = s3.put_object(**put_kwargs)
    return UploadResponse(
        bucket=request.bucket,
        key=request.key,
        etag=response.get("ETag"),
        version_id=response.get("VersionId"),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("bucket")
    parser.add_argument("key")
    parser.add_argument("body_path")
    parser.add_argument("--content-type")
    args = parser.parse_args()
    settings = load_settings()
    result = upload_object(UploadRequest(bucket=args.bucket or settings.bucket_name, key=args.key, body_path=args.body_path, content_type=args.content_type))
    print(dataclass_to_dict(result))
