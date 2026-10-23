from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional

from google.cloud import storage


GCS_CONTENT_TYPE = "application/json"


def archive_document_snapshots(bucket_name: str, records: Iterable[Dict[str, Any]], prefix: str = "exports", attachment_bytes: bytes | None = None, attachment_name: str | None = None) -> Dict[str, Optional[str]]:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    snapshot_blob_name = f"{prefix}/snapshot-{timestamp}.json"
    snapshot_blob = bucket.blob(snapshot_blob_name)
    snapshot_blob.upload_from_string(json.dumps(list(records), ensure_ascii=False, indent=2), content_type=GCS_CONTENT_TYPE)

    attachment_blob_name: Optional[str] = None
    if attachment_bytes is not None and attachment_name:
        attachment_blob_name = f"{prefix}/attachments/{timestamp}-{attachment_name}"
        attachment_blob = bucket.blob(attachment_blob_name)
        attachment_blob.upload_from_string(attachment_bytes)

    return {
        "provider": "Google Cloud Storage",
        "bucket": bucket_name,
        "snapshot_blob": snapshot_blob_name,
        "attachment_blob": attachment_blob_name,
    }
