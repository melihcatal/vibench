import base64
import hashlib
import json
import mimetypes
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional, Sequence

import boto3
from botocore.exceptions import ClientError


@dataclass
class ArchivedObject:
    key: str
    uri: str
    etag: Optional[str] = None
    version_id: Optional[str] = None


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _read_bytes(path: Path) -> bytes:
    return path.read_bytes()


def _build_s3_key(prefix: str, stem: str, suffix: str) -> str:
    prefix = prefix.strip("/")
    if prefix:
        return f"{prefix}/{stem}{suffix}"
    return f"{stem}{suffix}"


def archive_image_assets(
    image_path: str,
    captions: Sequence[str],
    bucket: str,
    prefix: str = "image-archive",
    region_name: Optional[str] = None,
) -> dict:
    image_file = Path(image_path)
    image_bytes = _read_bytes(image_file)
    image_hash = _sha256_bytes(image_bytes)
    caption_payload = {
        "source_image": image_file.name,
        "source_sha256": image_hash,
        "created_at": _utc_now(),
        "captions": list(captions),
    }
    derived_json = json.dumps(caption_payload, ensure_ascii=False, indent=2).encode("utf-8")
    manifest = {
        "image": image_file.name,
        "image_sha256": image_hash,
        "captions_sha256": _sha256_bytes(derived_json),
        "mime_type": mimetypes.guess_type(image_file.name)[0] or "application/octet-stream",
        "archived_at": _utc_now(),
    }

    s3 = boto3.client("s3", region_name=region_name)
    stem = image_file.stem
    image_key = _build_s3_key(prefix, stem, image_file.suffix)
    captions_key = _build_s3_key(prefix, stem, ".captions.json")
    manifest_key = _build_s3_key(prefix, stem, ".manifest.json")

    uploaded = []
    content_type = mimetypes.guess_type(image_file.name)[0] or "application/octet-stream"
    try:
        image_resp = s3.put_object(
            Bucket=bucket,
            Key=image_key,
            Body=image_bytes,
            ContentType=content_type,
            Metadata={"sha256": image_hash},
        )
        uploaded.append(
            ArchivedObject(
                key=image_key,
                uri=f"s3://{bucket}/{image_key}",
                etag=image_resp.get("ETag"),
                version_id=image_resp.get("VersionId"),
            )
        )
        captions_resp = s3.put_object(
            Bucket=bucket,
            Key=captions_key,
            Body=derived_json,
            ContentType="application/json",
            Metadata={"sha256": manifest["captions_sha256"]},
        )
        uploaded.append(
            ArchivedObject(
                key=captions_key,
                uri=f"s3://{bucket}/{captions_key}",
                etag=captions_resp.get("ETag"),
                version_id=captions_resp.get("VersionId"),
            )
        )
        manifest_resp = s3.put_object(
            Bucket=bucket,
            Key=manifest_key,
            Body=json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8"),
            ContentType="application/json",
            Metadata={"image_sha256": image_hash},
        )
        uploaded.append(
            ArchivedObject(
                key=manifest_key,
                uri=f"s3://{bucket}/{manifest_key}",
                etag=manifest_resp.get("ETag"),
                version_id=manifest_resp.get("VersionId"),
            )
        )
    except ClientError:
        raise

    return {
        "bucket": bucket,
        "uploaded": [obj.__dict__ for obj in uploaded],
        "manifest": manifest,
    }


def archive_directory(
    directory: str,
    bucket: str,
    prefix: str = "image-archive",
    region_name: Optional[str] = None,
    caption_suffixes: Iterable[str] = (".txt", ".json"),
) -> dict:
    root = Path(directory)
    s3 = boto3.client("s3", region_name=region_name)
    results = []
    for path in sorted(root.iterdir()):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".tif", ".tiff", ".bmp"}:
            continue
        captions = []
        for suffix in caption_suffixes:
            candidate = path.with_suffix(suffix)
            if candidate.exists():
                if candidate.suffix.lower() == ".json":
                    payload = json.loads(_read_text(candidate))
                    captions.extend(payload if isinstance(payload, list) else [json.dumps(payload, ensure_ascii=False)])
                else:
                    captions.extend([line for line in _read_text(candidate).splitlines() if line.strip()])
        results.append(archive_image_assets(str(path), captions, bucket, prefix=prefix, region_name=region_name))
    return {"bucket": bucket, "count": len(results), "results": results}


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Archive image-analysis artifacts to AWS S3.")
    parser.add_argument("image", nargs="?", help="Path to an image file")
    parser.add_argument("--captions", nargs="*", default=[], help="Derived captions to store")
    parser.add_argument("--directory", help="Archive images from a directory")
    parser.add_argument("--bucket", required=True, help="Amazon S3 bucket name")
    parser.add_argument("--prefix", default="image-archive", help="S3 key prefix")
    parser.add_argument("--region", default=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    args = parser.parse_args()

    if args.directory:
        print(json.dumps(archive_directory(args.directory, args.bucket, args.prefix, args.region), ensure_ascii=False))
        return
    if not args.image:
        raise SystemExit("image path or --directory is required")
    print(json.dumps(archive_image_assets(args.image, args.captions, args.bucket, args.prefix, args.region), ensure_ascii=False))


if __name__ == "__main__":
    main()
