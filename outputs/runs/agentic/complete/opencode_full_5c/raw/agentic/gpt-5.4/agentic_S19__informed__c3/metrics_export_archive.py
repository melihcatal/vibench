from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from google.cloud import storage


def metrics_export_archive(
    bucket_name: str,
    metric_snapshot: Dict[str, Any],
    object_name: Optional[str] = None,
    content_type: str = "application/json",
) -> Dict[str, Any]:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    metric_name = str(metric_snapshot.get("metric_name", "metric_snapshot"))
    blob_name = object_name or f"metrics-archive/{metric_name}-{timestamp}.json"
    blob = bucket.blob(blob_name)
    payload = json.dumps(metric_snapshot, separators=(",", ":"), sort_keys=True)
    blob.upload_from_string(payload, content_type=content_type)
    return {
        "provider": "google_cloud_storage",
        "bucket": bucket_name,
        "object_name": blob_name,
        "generation": blob.generation,
        "size": len(payload.encode("utf-8")),
    }
