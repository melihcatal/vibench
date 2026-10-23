from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

from google.cloud import storage


def archive_record_snapshot(record: dict[str, Any], prefix: str = "exports") -> str:
    client = storage.Client()
    bucket_name = os.environ["GCS_BUCKET_NAME"]
    bucket = client.bucket(bucket_name)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    record_id = str(record.get("id", "record"))
    object_name = f"{prefix}/{record_id}-{timestamp}.json"
    blob = bucket.blob(object_name)
    blob.upload_from_string(
        json.dumps(record, ensure_ascii=False), content_type="application/json"
    )
    return f"gs://{bucket_name}/{object_name}"
