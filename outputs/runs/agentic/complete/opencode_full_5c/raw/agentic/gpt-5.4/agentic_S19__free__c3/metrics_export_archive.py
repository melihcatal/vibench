from __future__ import annotations

import json
from datetime import datetime, timezone

from google.cloud import storage


def metrics_export_archive(
    bucket_name: str, object_name: str, snapshot: dict, project_id: str | None = None
) -> dict:
    client = storage.Client(project=project_id)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    payload = {
        "archived_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "snapshot": snapshot,
    }
    blob.upload_from_string(json.dumps(payload), content_type="application/json")
    return {
        "bucket": bucket_name,
        "object": object_name,
        "generation": blob.generation,
        "provider": "google-cloud-storage",
    }
