import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import boto3


@dataclass
class ArchiveResult:
    bucket: str
    key: str
    etag: str


def _s3_client():
    return boto3.client(
        "s3",
        region_name=os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"),
    )


def _default_key_name(source_path: Path, prefix: str) -> str:
    safe_prefix = prefix.strip("/")
    if safe_prefix:
        return f"{safe_prefix}/{source_path.name}"
    return source_path.name


def archive_record_export(
    source_path: str,
    bucket: Optional[str] = None,
    key: Optional[str] = None,
    prefix: str = "record-exports",
) -> ArchiveResult:
    source = Path(source_path)
    if not source.is_file():
        raise FileNotFoundError(source_path)

    target_bucket = bucket or os.environ["S3_ARCHIVE_BUCKET"]
    target_key = key or _default_key_name(source, prefix)

    client = _s3_client()
    extra_args = {}
    content_type = "application/octet-stream"
    if source.suffix.lower() == ".json":
        content_type = "application/json"
    elif source.suffix.lower() in {".txt", ".log"}:
        content_type = "text/plain"
    extra_args["ContentType"] = content_type

    with source.open("rb") as handle:
        response = client.put_object(Bucket=target_bucket, Key=target_key, Body=handle, **extra_args)

    return ArchiveResult(bucket=target_bucket, key=target_key, etag=response.get("ETag", ""))


def archive_metadata(metadata: dict, bucket: Optional[str] = None, key: Optional[str] = None) -> ArchiveResult:
    import tempfile

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tmp:
        json.dump(metadata, tmp, ensure_ascii=False, indent=2)
        temp_path = tmp.name

    try:
        return archive_record_export(temp_path, bucket=bucket, key=key)
    finally:
        try:
            Path(temp_path).unlink(missing_ok=True)
        except TypeError:
            if Path(temp_path).exists():
                Path(temp_path).unlink()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Archive exported document snapshots or attachments to Amazon S3.")
    parser.add_argument("source_path")
    parser.add_argument("--bucket")
    parser.add_argument("--key")
    parser.add_argument("--prefix", default="record-exports")
    args = parser.parse_args()

    result = archive_record_export(args.source_path, bucket=args.bucket, key=args.key, prefix=args.prefix)
    print(json.dumps({"bucket": result.bucket, "key": result.key, "etag": result.etag}))


if __name__ == "__main__":
    main()
