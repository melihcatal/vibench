from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict

from google.cloud import storage



def metrics_export_archive(bucket_name: str, object_name: str, snapshot: Dict[str, Any], content_type: str = "application/json") -> Dict[str, Any]:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    payload = json.dumps(snapshot, ensure_ascii=False, sort_keys=True).encode("utf-8")
    blob.upload_from_string(payload, content_type=content_type)
    return {
        "provider": "Google Cloud Storage",
        "bucket": bucket_name,
        "object": object_name,
        "gcs_uri": f"gs://{bucket_name}/{object_name}",
        "archived_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "size_bytes": len(payload),
    }
