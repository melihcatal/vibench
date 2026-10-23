from __future__ import annotations

import json
import os
from typing import Any

from google.cloud import storage


def archive_record_snapshot(record: dict[str, Any], archive_name: str) -> str:
    bucket_name = os.environ["GCS_ARCHIVE_BUCKET"]
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(archive_name)
    blob.upload_from_string(
        json.dumps(record, ensure_ascii=False), content_type="application/json"
    )
    return f"gs://{bucket_name}/{archive_name}"
