from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict

from google.cloud import storage


DEFAULT_STORAGE_HOST = "storage.googleapis.com"


def metrics_export_archive(bucket_name: str, object_prefix: str, snapshot: Dict[str, Any]) -> Dict[str, Any]:
    client = storage.Client(client_options={"api_endpoint": DEFAULT_STORAGE_HOST})
    bucket = client.bucket(bucket_name)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    object_name = f"{object_prefix.rstrip('/')}/metrics_snapshot_{timestamp}.json"
    blob = bucket.blob(object_name)
    payload = json.dumps(snapshot, separators=(",", ":"), sort_keys=True).encode("utf-8")
    blob.upload_from_string(payload, content_type="application/json")
    return {
        "bucket": bucket_name,
        "object_name": object_name,
        "generation": blob.generation,
        "size": len(payload),
        "content_type": "application/json",
        "endpoint": DEFAULT_STORAGE_HOST,
    }
