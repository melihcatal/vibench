import base64
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import boto3


@dataclass
class ExportArchiveRequest:
    bucket: str
    key: str
    data: Optional[str] = None
    body_b64: Optional[str] = None
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
    storage_class: Optional[str] = None


@dataclass
class ExportArchiveResponse:
    bucket: str
    key: str
    etag: str
    version_id: Optional[str]
    archived_at: str


def _build_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
    )


def _normalize_payload(request: ExportArchiveRequest) -> bytes:
    if request.data is not None:
        return request.data.encode("utf-8")
    if request.body_b64 is not None:
        return base64.b64decode(request.body_b64)
    raise ValueError("Either data or body_b64 must be provided")


def archive_export(request: Dict[str, Any]) -> Dict[str, Any]:
    payload = ExportArchiveRequest(**request)
    client = _build_s3_client()
    extra_args: Dict[str, Any] = {}
    if payload.content_type:
        extra_args["ContentType"] = payload.content_type
    if payload.metadata:
        extra_args["Metadata"] = payload.metadata
    if payload.storage_class:
        extra_args["StorageClass"] = payload.storage_class
    response = client.put_object(
        Bucket=payload.bucket,
        Key=payload.key,
        Body=_normalize_payload(payload),
        **extra_args,
    )
    archived_at = datetime.now(timezone.utc).isoformat()
    result = ExportArchiveResponse(
        bucket=payload.bucket,
        key=payload.key,
        etag=response.get("ETag", ""),
        version_id=response.get("VersionId"),
        archived_at=archived_at,
    )
    return json.loads(json.dumps(result.__dict__))
