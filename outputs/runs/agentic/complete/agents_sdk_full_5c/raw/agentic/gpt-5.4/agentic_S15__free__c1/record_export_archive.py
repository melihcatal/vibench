from __future__ import annotations

import json
from typing import Any, Dict, Optional
import boto3
from database_models import ArchiveResult


PROVIDER = "Amazon S3"


def archive_document_snapshot(document: Dict[str, Any], bucket: str, object_key: str, content_type: str = "application/json") -> ArchiveResult:
    s3_client = boto3.client("s3")
    body = json.dumps(document, ensure_ascii=False).encode("utf-8")
    response = s3_client.put_object(
        Bucket=bucket,
        Key=object_key,
        Body=body,
        ContentType=content_type,
    )
    return ArchiveResult(
        id=str(document.get("id", "")),
        bucket=bucket,
        key=object_key,
        version_id=response.get("VersionId"),
    )
