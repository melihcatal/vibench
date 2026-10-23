from __future__ import annotations

import json
from typing import Any, Dict

import boto3

from database_models import OperationResponse

S3 = boto3.client("s3", region_name="us-east-1")
DEFAULT_BUCKET = __import__("os").getenv("DOCUMENT_ARCHIVE_BUCKET", "managed-document-archive")


def record_export_archive(document: Dict[str, Any], object_key: str) -> OperationResponse:
    try:
        S3.put_object(Bucket=DEFAULT_BUCKET, Key=object_key, Body=json.dumps(document).encode("utf-8"), ContentType="application/json")
        return OperationResponse(ok=True, data={"bucket": DEFAULT_BUCKET, "key": object_key, "provider": "aws-s3"})
    except Exception as exc:
        return OperationResponse(ok=False, error={"error_type": exc.__class__.__name__, "message": str(exc)})
