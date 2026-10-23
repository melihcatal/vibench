from __future__ import annotations

import base64
import hashlib
import json
import mimetypes
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional

import requests


S3_ENDPOINT_ENV = "AWS_S3_ENDPOINT_URL"
S3_BUCKET_ENV = "AWS_S3_BUCKET"
S3_REGION_ENV = "AWS_REGION"
S3_ACCESS_KEY_ENV = "AWS_ACCESS_KEY_ID"
S3_SECRET_KEY_ENV = "AWS_SECRET_ACCESS_KEY"
S3_SESSION_TOKEN_ENV = "AWS_SESSION_TOKEN"
S3_STORAGE_CLASS_ENV = "AWS_S3_STORAGE_CLASS"


@dataclass(frozen=True)
class ArchiveConfig:
    endpoint_url: str
    bucket: str
    region: str
    access_key_id: str
    secret_access_key: str
    session_token: Optional[str] = None
    storage_class: str = "STANDARD"


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise ValueError(f"{name} is required")
    return value


def load_config() -> ArchiveConfig:
    return ArchiveConfig(
        endpoint_url=os.environ.get(S3_ENDPOINT_ENV, "https://s3.amazonaws.com").rstrip("/"),
        bucket=_require_env(S3_BUCKET_ENV),
        region=os.environ.get(S3_REGION_ENV, "us-east-1"),
        access_key_id=_require_env(S3_ACCESS_KEY_ENV),
        secret_access_key=_require_env(S3_SECRET_KEY_ENV),
        session_token=os.environ.get(S3_SESSION_TOKEN_ENV),
        storage_class=os.environ.get(S3_STORAGE_CLASS_ENV, "STANDARD"),
    )


def _normalize_payload(payload: Any) -> bytes:
    if isinstance(payload, bytes):
        return payload
    if isinstance(payload, str):
        return payload.encode("utf-8")
    if isinstance(payload, (dict, list)):
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    if hasattr(payload, "read"):
        data = payload.read()
        return data if isinstance(data, bytes) else str(data).encode("utf-8")
    return str(payload).encode("utf-8")


def _extract_source(record: Any) -> Dict[str, Any]:
    if isinstance(record, dict):
        return record
    if hasattr(record, "model_dump"):
        dumped = record.model_dump()
        if isinstance(dumped, dict):
            return dumped
    if hasattr(record, "dict"):
        dumped = record.dict()
        if isinstance(dumped, dict):
            return dumped
    return {"value": record}


def _guess_content_type(name: str, default: str = "application/octet-stream") -> str:
    return mimetypes.guess_type(name)[0] or default


def _s3_url(config: ArchiveConfig, key: str) -> str:
    return f"{config.endpoint_url}/{config.bucket}/{key.lstrip('/')}"


def archive_exported_document_snapshot(snapshot: Any, object_key: Optional[str] = None) -> Dict[str, Any]:
    config = load_config()
    source = _extract_source(snapshot)
    key = object_key or source.get("object_key") or source.get("key") or source.get("id")
    if not key:
        digest = hashlib.sha256(_normalize_payload(source)).hexdigest()
        key = f"document-exports/{digest}.json"
    key = str(key)
    body = _normalize_payload(source)
    headers = {
        "Content-Type": _guess_content_type(key, "application/json"),
        "x-amz-storage-class": config.storage_class,
        "x-amz-content-sha256": hashlib.sha256(body).hexdigest(),
    }
    if config.session_token:
        headers["x-amz-security-token"] = config.session_token
    response = requests.put(
        _s3_url(config, key),
        data=body,
        headers=headers,
        auth=(config.access_key_id, config.secret_access_key),
        timeout=60,
    )
    response.raise_for_status()
    return {
        "bucket": config.bucket,
        "key": key,
        "region": config.region,
        "storage_class": config.storage_class,
        "etag": response.headers.get("ETag", ""),
        "content_type": headers["Content-Type"],
        "url": _s3_url(config, key),
    }


def archive_exported_document_attachment(data: Any, filename: str, prefix: str = "attachments/") -> Dict[str, Any]:
    key = f"{prefix.rstrip('/')}/{filename.lstrip('/')}" if prefix else filename
    return archive_exported_document_snapshot(data, object_key=key)
