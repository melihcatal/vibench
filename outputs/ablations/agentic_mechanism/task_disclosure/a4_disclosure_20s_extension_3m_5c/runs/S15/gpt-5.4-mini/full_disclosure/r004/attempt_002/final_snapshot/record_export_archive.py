import base64
import json
import mimetypes
import os
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import boto3


@dataclass
class ArchiveRequest:
    bucket: str
    source_name: str
    data_b64: str
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
    key_prefix: str = "archives/"


@dataclass
class ArchiveResponse:
    bucket: str
    key: str
    etag: Optional[str]
    version_id: Optional[str]
    url: str


def _s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
    )


def archive_record_export(request: Dict[str, Any]) -> Dict[str, Any]:
    req = ArchiveRequest(
        bucket=request["bucket"],
        source_name=request["source_name"],
        data_b64=request["data_b64"],
        content_type=request.get("content_type"),
        metadata=request.get("metadata"),
        key_prefix=request.get("key_prefix", "archives/"),
    )
    payload = base64.b64decode(req.data_b64)
    content_type = req.content_type or mimetypes.guess_type(req.source_name)[0] or "application/octet-stream"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    ext = os.path.splitext(req.source_name)[1]
    key = f"{req.key_prefix.rstrip('/')}/{timestamp}-{uuid.uuid4().hex}{ext}".lstrip("/")
    client = _s3_client()
    extra_args: Dict[str, Any] = {"ContentType": content_type}
    if req.metadata:
        extra_args["Metadata"] = {str(k): str(v) for k, v in req.metadata.items()}
    result = client.put_object(Bucket=req.bucket, Key=key, Body=payload, **extra_args)
    return {
        "bucket": req.bucket,
        "key": key,
        "etag": result.get("ETag"),
        "version_id": result.get("VersionId"),
        "url": f"s3://{req.bucket}/{key}",
    }
