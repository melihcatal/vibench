import base64
import hashlib
import json
import mimetypes
import os
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional, Sequence, Tuple

import boto3
from botocore.exceptions import BotoCoreError, ClientError


@dataclass
class ArchivedArtifact:
    key: str
    content_type: str
    bytes_written: int
    etag: Optional[str] = None


@dataclass
class ArchiveResult:
    bucket: str
    prefix: str
    image_key: str
    metadata_key: str
    captions_key: Optional[str]
    artifacts: Sequence[ArchivedArtifact]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bucket": self.bucket,
            "prefix": self.prefix,
            "image_key": self.image_key,
            "metadata_key": self.metadata_key,
            "captions_key": self.captions_key,
            "artifacts": [asdict(item) for item in self.artifacts],
        }


def _s3_client():
    return boto3.client("s3")


def _guess_content_type(path: str, default: str = "application/octet-stream") -> str:
    guessed, _ = mimetypes.guess_type(path)
    return guessed or default


def _safe_prefix(prefix: str) -> str:
    prefix = prefix.strip("/")
    if prefix:
        return prefix + "/"
    return ""


def _timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_bytes(source: Any) -> bytes:
    if isinstance(source, bytes):
        return source
    if isinstance(source, bytearray):
        return bytes(source)
    if isinstance(source, str):
        if os.path.exists(source):
            with open(source, "rb") as fh:
                return fh.read()
        try:
            return base64.b64decode(source, validate=True)
        except Exception as exc:
            raise ValueError("source must be a file path, bytes, or base64-encoded string") from exc
    raise TypeError("source must be a file path, bytes, bytearray, or base64 string")


def archive_image_analysis(
    image_source: Any,
    captions: Optional[Sequence[str]] = None,
    analysis: Optional[Dict[str, Any]] = None,
    bucket: Optional[str] = None,
    prefix: str = "image-asset-archive",
    image_filename: Optional[str] = None,
) -> ArchiveResult:
    bucket_name = bucket or os.environ.get("AWS_S3_BUCKET") or os.environ.get("S3_BUCKET")
    if not bucket_name:
        raise ValueError("bucket is required; set AWS_S3_BUCKET or S3_BUCKET")

    s3 = _s3_client()
    data = _read_bytes(image_source)
    digest = _digest(data)
    stamp = _timestamp()
    normalized_prefix = _safe_prefix(prefix)

    if image_filename:
        base_name = os.path.basename(image_filename)
    else:
        base_name = f"image-{digest[:16]}.bin"

    image_key = f"{normalized_prefix}{stamp}-{digest[:12]}/{base_name}"
    metadata_key = f"{normalized_prefix}{stamp}-{digest[:12]}/metadata.json"
    captions_key = None
    artifacts = []

    content_type = _guess_content_type(image_filename or base_name)
    try:
        put_response = s3.put_object(
            Bucket=bucket_name,
            Key=image_key,
            Body=data,
            ContentType=content_type,
            Metadata={"sha256": digest, "source": "image_asset_archive.py"},
        )
        artifacts.append(
            ArchivedArtifact(
                key=image_key,
                content_type=content_type,
                bytes_written=len(data),
                etag=put_response.get("ETag"),
            )
        )

        payload = {
            "archived_at": stamp,
            "bucket": bucket_name,
            "image_key": image_key,
            "image_sha256": digest,
            "captions": list(captions or []),
            "analysis": analysis or {},
            "source_filename": image_filename,
        }
        metadata_bytes = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8")
        meta_put = s3.put_object(
            Bucket=bucket_name,
            Key=metadata_key,
            Body=metadata_bytes,
            ContentType="application/json",
            Metadata={"sha256": _digest(metadata_bytes), "source": "image_asset_archive.py"},
        )
        artifacts.append(
            ArchivedArtifact(
                key=metadata_key,
                content_type="application/json",
                bytes_written=len(metadata_bytes),
                etag=meta_put.get("ETag"),
            )
        )

        if captions:
            captions_key = f"{normalized_prefix}{stamp}-{digest[:12]}/captions.txt"
            captions_bytes = ("\n".join(captions) + "\n").encode("utf-8")
            cap_put = s3.put_object(
                Bucket=bucket_name,
                Key=captions_key,
                Body=captions_bytes,
                ContentType="text/plain; charset=utf-8",
                Metadata={"sha256": _digest(captions_bytes), "source": "image_asset_archive.py"},
            )
            artifacts.append(
                ArchivedArtifact(
                    key=captions_key,
                    content_type="text/plain; charset=utf-8",
                    bytes_written=len(captions_bytes),
                    etag=cap_put.get("ETag"),
                )
            )
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"failed to archive image assets to Amazon S3: {exc}") from exc

    return ArchiveResult(
        bucket=bucket_name,
        prefix=normalized_prefix.rstrip("/"),
        image_key=image_key,
        metadata_key=metadata_key,
        captions_key=captions_key,
        artifacts=artifacts,
    )


def archive_image_asset_from_paths(
    image_path: str,
    captions: Optional[Sequence[str]] = None,
    analysis: Optional[Dict[str, Any]] = None,
    bucket: Optional[str] = None,
    prefix: str = "image-asset-archive",
) -> Dict[str, Any]:
    result = archive_image_analysis(
        image_source=image_path,
        captions=captions,
        analysis=analysis,
        bucket=bucket,
        prefix=prefix,
        image_filename=os.path.basename(image_path),
    )
    return result.to_dict()
