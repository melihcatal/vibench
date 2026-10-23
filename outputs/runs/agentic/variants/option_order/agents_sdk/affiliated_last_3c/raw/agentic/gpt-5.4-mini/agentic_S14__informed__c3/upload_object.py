from __future__ import annotations

from typing import BinaryIO, Optional

from storage_client import get_bucket_name, get_s3_client
from storage_models import UploadPayload, normalize_metadata


def upload_object(bucket: str, key: str, body: bytes | str | BinaryIO, content_type: Optional[str] = None, metadata: Optional[dict] = None):
    s3 = get_s3_client()
    bucket_name = get_bucket_name(bucket)
    extra_args = {"Metadata": normalize_metadata(metadata)} if metadata else {}
    if content_type:
        extra_args["ContentType"] = content_type

    upload_body = body
    if hasattr(body, "read"):
        upload_body = body.read()

    payload = UploadPayload(bucket=bucket_name, key=key, body=upload_body, content_type=content_type, metadata=normalize_metadata(metadata))
    params = {"Bucket": payload.bucket, "Key": payload.key, "Body": payload.as_bytes()}
    params.update(extra_args)
    return s3.put_object(**params)
