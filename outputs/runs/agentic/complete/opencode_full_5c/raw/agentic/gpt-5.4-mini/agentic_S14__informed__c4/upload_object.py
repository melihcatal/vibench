from pathlib import Path

from storage_client import client, load_config
from storage_models import ObjectResult


def upload_object(
    bucket: str,
    key: str,
    file_path: str | None = None,
    data: bytes | None = None,
    content_type: str | None = None,
) -> ObjectResult:
    s3 = client()
    body = data if data is not None else Path(file_path).read_bytes()
    extra = {}
    if content_type:
        extra["ContentType"] = content_type
    resp = s3.put_object(Bucket=bucket, Key=key, Body=body, **extra)
    return ObjectResult(
        bucket=bucket, key=key, etag=resp.get("ETag"), version_id=resp.get("VersionId")
    )


def main():
    cfg = load_config()
    raise SystemExit("bucket and key required")
