import base64
import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional
import boto3
from botocore.exceptions import BotoCoreError, ClientError


@dataclass
class ArchiveResult:
    bucket: str
    key: str
    metadata_key: str
    caption_key: Optional[str]
    etag: str


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _normalize_bytes(data: Any) -> bytes:
    if isinstance(data, bytes):
        return data
    if isinstance(data, str):
        if os.path.exists(data):
            with open(data, "rb") as f:
                return f.read()
        return data.encode("utf-8")
    if isinstance(data, dict) and "base64" in data:
        return base64.b64decode(data["base64"])
    raise TypeError("Unsupported artifact payload type")


def archive_image_analysis_artifacts(
    image_bytes: Any,
    analysis: Dict[str, Any],
    caption: Optional[str] = None,
    bucket: Optional[str] = None,
    prefix: str = "image-analysis",
    s3_client: Any = None,
) -> ArchiveResult:
    bucket_name = bucket or os.environ.get("AWS_S3_BUCKET")
    if not bucket_name:
        raise ValueError("Missing S3 bucket name; set bucket or AWS_S3_BUCKET")

    client = s3_client or boto3.client("s3")
    image_payload = _normalize_bytes(image_bytes)
    image_hash = _sha256_bytes(image_payload)
    analysis_hash = _sha256_bytes(json.dumps(analysis, sort_keys=True, ensure_ascii=False).encode("utf-8"))
    artifact_id = f"{image_hash[:16]}-{analysis_hash[:16]}"
    base_key = f"{prefix.rstrip('/')}/{artifact_id}"

    image_key = f"{base_key}/image.bin"
    metadata_key = f"{base_key}/analysis.json"
    caption_key = f"{base_key}/caption.txt" if caption is not None else None

    extra_args = {"ContentType": "application/octet-stream"}
    if "put_object" in dir(client):
        client.put_object(Bucket=bucket_name, Key=image_key, Body=image_payload, **extra_args)
        client.put_object(
            Bucket=bucket_name,
            Key=metadata_key,
            Body=json.dumps(
                {
                    "created_at": _utc_now(),
                    "image_sha256": image_hash,
                    "analysis_sha256": analysis_hash,
                    "analysis": analysis,
                },
                ensure_ascii=False,
                sort_keys=True,
                indent=2,
            ).encode("utf-8"),
            ContentType="application/json",
        )
        if caption_key:
            client.put_object(
                Bucket=bucket_name,
                Key=caption_key,
                Body=caption.encode("utf-8"),
                ContentType="text/plain; charset=utf-8",
            )
        etag = client.head_object(Bucket=bucket_name, Key=image_key)["ETag"].strip('"')
    else:
        raise TypeError("s3_client must provide put_object and head_object")

    return ArchiveResult(
        bucket=bucket_name,
        key=image_key,
        metadata_key=metadata_key,
        caption_key=caption_key,
        etag=etag,
    )


def archive_from_base64(
    image_base64: str,
    analysis: Dict[str, Any],
    caption: Optional[str] = None,
    bucket: Optional[str] = None,
    prefix: str = "image-analysis",
    s3_client: Any = None,
) -> ArchiveResult:
    return archive_image_analysis_artifacts(
        {"base64": image_base64},
        analysis,
        caption=caption,
        bucket=bucket,
        prefix=prefix,
        s3_client=s3_client,
    )


__all__ = ["ArchiveResult", "archive_image_analysis_artifacts", "archive_from_base64"]
