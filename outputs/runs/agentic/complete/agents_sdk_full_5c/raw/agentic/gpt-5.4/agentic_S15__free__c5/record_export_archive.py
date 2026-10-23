from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, Iterable
from uuid import uuid4

from google.cloud import storage


GCS_BUCKET_ENV = "GCS_ARCHIVE_BUCKET"


def record_export_archive(records: Iterable[Dict[str, Any]], prefix: str = "exports") -> str:
    client = storage.Client()
    bucket = client.bucket(os.environ[GCS_BUCKET_ENV])
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    blob_name = f"{prefix}/document-snapshot-{timestamp}-{uuid4().hex}.json"
    blob = bucket.blob(blob_name)
    blob.upload_from_string(
        json.dumps(list(records), ensure_ascii=False, default=str, indent=2),
        content_type="application/json",
    )
    return f"gs://{bucket.name}/{blob_name}"
