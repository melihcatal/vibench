from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from google.cloud import storage


def metrics_export_archive(bucket_name: str, object_name: str, payload: bytes) -> Dict[str, Any]:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_string(payload, content_type="application/octet-stream")
    return {"bucket": bucket_name, "object": object_name, "archived_at": datetime.now(timezone.utc).isoformat(), "provider": "google-cloud-storage"}
