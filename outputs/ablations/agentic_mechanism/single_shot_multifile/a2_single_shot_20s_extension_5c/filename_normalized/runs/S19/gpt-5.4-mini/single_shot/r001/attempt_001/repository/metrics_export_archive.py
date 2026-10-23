from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict

from google.cloud import storage


def metrics_export_archive(bucket_name: str, object_name: str, payload: bytes) -> Dict[str, object]:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_string(payload)
    return {"bucket": bucket_name, "object_name": object_name, "updated": datetime.now(timezone.utc).isoformat()}
