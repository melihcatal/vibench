import base64
import hashlib
import json
import mimetypes
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3


S3_BUCKET = os.getenv("AWS_S3_BUCKET", "")
AWS_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))


@dataclass
class ArchiveResult:
    bucket: str
    image_key: str
    artifact_key: str
    caption_key: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


def _load_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _guess_content_type(path: str) -> str:
    content_type, _ = mimetypes.guess_type(path)
    return content_type or "application/octet-stream"


def _normalize_payload(value: Any) -> bytes:
    if value is None:
        return b""
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode("utf-8")
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8")


def _client():
    return boto3.client("s3", region_name=AWS_REGION)


def archive_image_analysis(
    image_path: str,
    analysis_artifacts: Any = None,
    caption: Optional[str] = None,
    bucket: Optional[str] = None,
    prefix: str = "image-analysis",
) -> ArchiveResult:
    target_bucket = bucket or S3_BUCKET
    if not target_bucket:
        raise ValueError("AWS_S3_BUCKET is required")

    image_bytes = _load_bytes(image_path)
    image_hash = _sha256_hex(image_bytes)
    image_name = os.path.basename(image_path)
    image_key = f"{prefix}/images/{image_hash}/{image_name}"
    artifact_key = f"{prefix}/artifacts/{image_hash}.json"
    caption_key = f"{prefix}/captions/{image_hash}.txt" if caption is not None else None

    client = _client()
    client.put_object(
        Bucket=target_bucket,
        Key=image_key,
        Body=image_bytes,
        ContentType=_guess_content_type(image_path),
        Metadata={"sha256": image_hash},
    )

    artifact_bytes = _normalize_payload(analysis_artifacts)
    client.put_object(
        Bucket=target_bucket,
        Key=artifact_key,
        Body=artifact_bytes,
        ContentType="application/json",
        Metadata={"sha256": image_hash},
    )

    if caption_key is not None:
        client.put_object(
            Bucket=target_bucket,
            Key=caption_key,
            Body=_normalize_payload(caption),
            ContentType="text/plain; charset=utf-8",
            Metadata={"sha256": image_hash},
        )

    return ArchiveResult(
        bucket=target_bucket,
        image_key=image_key,
        artifact_key=artifact_key,
        caption_key=caption_key,
        metadata={"sha256": image_hash, "region": AWS_REGION},
    )


def archive_image_analysis_from_base64(
    image_base64: str,
    image_name: str,
    analysis_artifacts: Any = None,
    caption: Optional[str] = None,
    bucket: Optional[str] = None,
    prefix: str = "image-analysis",
) -> ArchiveResult:
    image_bytes = base64.b64decode(image_base64)
    temp_path = os.path.join("/tmp", image_name)
    with open(temp_path, "wb") as f:
        f.write(image_bytes)
    return archive_image_analysis(temp_path, analysis_artifacts=analysis_artifacts, caption=caption, bucket=bucket, prefix=prefix)
