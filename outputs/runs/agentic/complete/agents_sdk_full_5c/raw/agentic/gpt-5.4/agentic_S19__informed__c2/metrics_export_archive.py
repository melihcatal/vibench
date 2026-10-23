from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict

from google.cloud import storage


DEFAULT_CONTENT_TYPE = "application/json"


def metrics_export_archive(snapshot: Dict[str, Any], bucket_name: str, prefix: str = "metrics-archive") -> str:
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS must be set for Google Cloud Storage access")

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    blob_name = f"{prefix}/snapshot-{timestamp}.json"
    blob = bucket.blob(blob_name)
    blob.upload_from_string(json.dumps(snapshot, ensure_ascii=False, default=str), content_type=DEFAULT_CONTENT_TYPE)
    return f"gs://{bucket_name}/{blob_name}"
