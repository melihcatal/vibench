import os
import mimetypes
from pathlib import Path
from datetime import datetime, timezone

import boto3
from botocore.exceptions import BotoCoreError, ClientError


S3_BUCKET_ENV = "ARCHIVE_S3_BUCKET"
S3_PREFIX_ENV = "ARCHIVE_S3_PREFIX"
AWS_REGION_ENV = "AWS_REGION"


def _s3_client():
    region = os.environ.get(AWS_REGION_ENV)
    if region:
        return boto3.client("s3", region_name=region)
    return boto3.client("s3")


def _archive_key(source_path: Path, prefix: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    name = source_path.name
    if prefix:
        prefix = prefix.strip("/")
        return f"{prefix}/{stamp}/{name}"
    return f"{stamp}/{name}"


def archive_export(path: str, bucket: str | None = None, key_prefix: str | None = None) -> str:
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(path)

    bucket_name = bucket or os.environ.get(S3_BUCKET_ENV)
    if not bucket_name:
        raise ValueError(f"Missing S3 bucket. Set {S3_BUCKET_ENV} or pass bucket.")

    prefix = key_prefix if key_prefix is not None else os.environ.get(S3_PREFIX_ENV, "exports")
    key = _archive_key(source, prefix)
    content_type, _ = mimetypes.guess_type(source.name)
    extra_args = {"ContentType": content_type} if content_type else {}

    s3 = _s3_client()
    try:
        s3.upload_file(str(source), bucket_name, key, ExtraArgs=extra_args or None)
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"Failed to archive {path} to s3://{bucket_name}/{key}") from exc

    return f"s3://{bucket_name}/{key}"


def archive_exports(paths: list[str], bucket: str | None = None, key_prefix: str | None = None) -> list[str]:
    return [archive_export(path, bucket=bucket, key_prefix=key_prefix) for path in paths]


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("Usage: record_export_archive.py <file> [<file> ...]")
    results = archive_exports(sys.argv[1:])
    for item in results:
        print(item)
