import base64
import hashlib
import mimetypes
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional, Union

import boto3
from botocore.exceptions import BotoCoreError, ClientError


@dataclass
class ArchivedImageAsset:
    bucket: str
    prefix: str
    manifest_key: str
    artifact_keys: Dict[str, str]
    caption_key: Optional[str]


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_bytes(value: Union[str, bytes, bytearray]) -> bytes:
    if isinstance(value, (bytes, bytearray)):
        return bytes(value)
    if isinstance(value, str):
        if os.path.exists(value):
            with open(value, "rb") as f:
                return f.read()
        try:
            return base64.b64decode(value, validate=True)
        except Exception as exc:
            raise ValueError("Expected a file path or base64-encoded string") from exc
    raise TypeError("Unsupported input type")


def _guess_content_type(key: str) -> str:
    return mimetypes.guess_type(key)[0] or "application/octet-stream"


def archive_image_assets(
    image: Union[str, bytes, bytearray],
    artifacts: Optional[Dict[str, Union[str, bytes, bytearray, Dict[str, Any], list]]] = None,
    caption: Optional[str] = None,
    bucket: Optional[str] = None,
    prefix: str = "image-archive",
    s3_client: Any = None,
) -> ArchivedImageAsset:
    bucket_name = bucket or os.environ.get("AWS_S3_BUCKET") or os.environ.get("IMAGE_ARCHIVE_BUCKET")
    if not bucket_name:
        raise ValueError("A target S3 bucket is required")
    client = s3_client or boto3.client("s3")
    image_bytes = _load_bytes(image)
    image_hash = _sha256_bytes(image_bytes)
    run_id = f"{_utc_now()}-{image_hash[:12]}"
    base_prefix = f"{prefix.rstrip('/')}/{run_id}"

    artifact_keys: Dict[str, str] = {}
    uploaded: Dict[str, bytes] = {"image": image_bytes}
    if artifacts:
        for name, value in artifacts.items():
            if isinstance(value, (dict, list)):
                payload = str(value).encode("utf-8")
            else:
                payload = _load_bytes(value)
            uploaded[name] = payload

    for name, payload in uploaded.items():
        key = f"{base_prefix}/{name}"
        client.put_object(Bucket=bucket_name, Key=key, Body=payload, ContentType=_guess_content_type(key))
        artifact_keys[name] = key

    caption_key = None
    if caption is not None:
        caption_key = f"{base_prefix}/caption.txt"
        client.put_object(Bucket=bucket_name, Key=caption_key, Body=caption.encode("utf-8"), ContentType="text/plain; charset=utf-8")

    manifest = {
        "bucket": bucket_name,
        "prefix": base_prefix,
        "image_sha256": image_hash,
        "artifacts": artifact_keys,
        "caption_key": caption_key,
        "created_at": _utc_now(),
        "provider": "aws-s3",
    }
    manifest_key = f"{base_prefix}/manifest.json"
    client.put_object(Bucket=bucket_name, Key=manifest_key, Body=str(manifest).encode("utf-8"), ContentType="application/json")
    return ArchivedImageAsset(bucket=bucket_name, prefix=base_prefix, manifest_key=manifest_key, artifact_keys=artifact_keys, caption_key=caption_key)


def archive_image_description(
    image: Union[str, bytes, bytearray],
    description: str,
    bucket: Optional[str] = None,
    prefix: str = "image-archive",
    s3_client: Any = None,
) -> ArchivedImageAsset:
    return archive_image_assets(image=image, artifacts=None, caption=description, bucket=bucket, prefix=prefix, s3_client=s3_client)


def normalize_archive_input(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "image": payload.get("image") or payload.get("image_data") or payload.get("path"),
        "artifacts": payload.get("artifacts") or {},
        "caption": payload.get("caption") or payload.get("description"),
        "bucket": payload.get("bucket") or payload.get("s3_bucket"),
        "prefix": payload.get("prefix") or "image-archive",
    }


__all__ = [
    "ArchivedImageAsset",
    "archive_image_assets",
    "archive_image_description",
    "normalize_archive_input",
]
