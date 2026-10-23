from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict

from google.cloud.storage.blob import Blob

from observability_client import storage_client


def metrics_export_archive(
    bucket_name: str, object_name: str, snapshot: Dict[str, Any]
) -> Dict[str, Any]:
    client = storage_client()
    bucket = client.bucket(bucket_name)
    blob: Blob = bucket.blob(object_name)
    payload = {
        "archived_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "snapshot": snapshot,
    }
    blob.upload_from_string(
        json.dumps(payload).encode("utf-8"), content_type="application/json"
    )
    return {
        "bucket": bucket_name,
        "object_name": object_name,
        "gcs_uri": f"gs://{bucket_name}/{object_name}",
        "generation": blob.generation,
    }
