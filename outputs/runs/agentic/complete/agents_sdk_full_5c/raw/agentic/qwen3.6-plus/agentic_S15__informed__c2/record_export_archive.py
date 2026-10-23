"""Archive exported document snapshots in Amazon S3.

Provider: Amazon S3 (boto3)
Auth env: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

from __future__ import annotations

import io
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

from database_models import DocumentResponse


_DEFAULT_BUCKET = os.environ.get("S3_ARCHIVE_BUCKET", "document-archives")
_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")


def _get_s3_client() -> boto3.client:
    """Create an S3 client using AWS credentials from the environment."""
    return boto3.client(
        "s3",
        region_name=_DEFAULT_REGION,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )


def _build_archive_key(prefix: Optional[str] = None) -> str:
    """Generate a unique S3 object key for an archive snapshot."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    parts = ["archives", ts, "documents.json"]
    if prefix:
        parts.insert(2, prefix)
    return "/".join(parts)


def archive_documents(
    records: List[DocumentResponse],
    bucket: Optional[str] = None,
    prefix: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Serialize and upload document snapshots to an S3 archive bucket."""
    bucket_name = bucket or _DEFAULT_BUCKET
    s3 = _get_s3_client()
    object_key = _build_archive_key(prefix)

    payload = {
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "record_count": len(records),
        "records": [
            {
                "doc_id": r.doc_id,
                "version": r.version,
                "data": r.data,
            }
            for r in records
        ],
    }

    body_bytes = json.dumps(payload, indent=2, default=str).encode("utf-8")
    fileobj = io.BytesIO(body_bytes)

    extra_args: Dict[str, Any] = {
        "ContentType": "application/json",
        "ServerSideEncryption": "AES256",
    }
    if metadata:
        extra_args["Metadata"] = metadata

    try:
        s3.upload_fileobj(
            fileobj,
            bucket_name,
            object_key,
            ExtraArgs=extra_args,
        )
    except ClientError as exc:
        raise RuntimeError(f"S3 upload failed: {exc}") from exc

    return {
        "bucket": bucket_name,
        "key": object_key,
        "size_bytes": len(body_bytes),
        "record_count": len(records),
    }


if __name__ == "__main__":
    sample = [
        DocumentResponse(doc_id="doc-1", data={"title": "Report"}, version=1, found=True),
    ]
    info = archive_documents(sample)
    print(f"Archived to s3://{info['bucket']}/{info['key']} ({info['size_bytes']} bytes)")
