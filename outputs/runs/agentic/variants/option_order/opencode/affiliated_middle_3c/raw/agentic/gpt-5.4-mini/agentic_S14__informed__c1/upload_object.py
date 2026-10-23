import base64
from pathlib import Path

from storage_client import get_bucket_name, get_s3_client
from storage_models import ObjectUploadResult, normalize_key


def upload_object(
    key: str, content: bytes | str | Path, content_type: str | None = None
) -> ObjectUploadResult:
    bucket = get_bucket_name()
    s3 = get_s3_client()
    object_key = normalize_key(key)
    if isinstance(content, Path):
        body = content.read_bytes()
    elif isinstance(content, str):
        body = content.encode("utf-8")
    else:
        body = content
    extra_args = {}
    if content_type:
        extra_args["ContentType"] = content_type
    response = s3.put_object(Bucket=bucket, Key=object_key, Body=body, **extra_args)
    return ObjectUploadResult(bucket=bucket, key=object_key, etag=response.get("ETag"))


def upload_base64_object(
    key: str, data_b64: str, content_type: str | None = None
) -> ObjectUploadResult:
    return upload_object(key, base64.b64decode(data_b64), content_type=content_type)
