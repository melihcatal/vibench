import json
import os
import mimetypes
from pathlib import Path

import boto3


def _env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name, default)
    return value if value not in ("", None) else None


def _s3_client():
    session_kwargs = {}
    region = _env("AWS_REGION") or _env("AWS_DEFAULT_REGION")
    if region:
        session_kwargs["region_name"] = region
    session = boto3.session.Session(**session_kwargs)
    return session.client("s3")


def _archive_key(prefix: str, source: Path, suffix: str) -> str:
    name = source.stem
    ext = source.suffix.lower()
    safe_prefix = prefix.strip("/")
    parts = [part for part in (safe_prefix, f"{name}{suffix}{ext}") if part]
    return "/".join(parts)


def archive_image_assets(
    image_path: str,
    caption_text: str,
    bucket_name: str | None = None,
    prefix: str = "image-archive",
) -> dict:
    source = Path(image_path)
    if not source.is_file():
        raise FileNotFoundError(image_path)

    bucket = bucket_name or _env("S3_BUCKET_NAME")
    if not bucket:
        raise ValueError("bucket_name or S3_BUCKET_NAME is required")

    client = _s3_client()
    content_type, _ = mimetypes.guess_type(source.name)
    image_key = _archive_key(prefix, source, "")
    caption_key = _archive_key(prefix, source, ".caption")
    metadata_key = _archive_key(prefix, source, ".metadata")

    extra_args = {"ContentType": content_type or "application/octet-stream"}
    client.upload_file(str(source), bucket, image_key, ExtraArgs=extra_args)
    client.put_object(
        Bucket=bucket,
        Key=caption_key,
        Body=caption_text.encode("utf-8"),
        ContentType="text/plain; charset=utf-8",
    )
    client.put_object(
        Bucket=bucket,
        Key=metadata_key,
        Body=json.dumps(
            {
                "source_file": source.name,
                "caption_key": caption_key,
                "image_key": image_key,
                "content_type": content_type,
            },
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8"),
        ContentType="application/json",
    )

    return {
        "bucket": bucket,
        "image_key": image_key,
        "caption_key": caption_key,
        "metadata_key": metadata_key,
        "provider": "aws-s3",
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Archive image artifacts to Amazon S3")
    parser.add_argument("image_path")
    parser.add_argument("caption_text")
    parser.add_argument("--bucket", dest="bucket_name")
    parser.add_argument("--prefix", default="image-archive")
    args = parser.parse_args()
    result = archive_image_assets(
        args.image_path,
        args.caption_text,
        bucket_name=args.bucket_name,
        prefix=args.prefix,
    )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
