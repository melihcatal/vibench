from __future__ import annotations

import json
import os
from typing import Any

from google.cloud import storage


def record_export_archive(
    document: dict[str, Any], archive_name: str
) -> dict[str, str]:
    client = storage.Client()
    bucket = client.bucket(os.environ["GCS_BUCKET_NAME"])
    blob = bucket.blob(f"document-archives/{archive_name}.json")
    blob.upload_from_string(
        json.dumps(document, separators=(",", ":")), content_type="application/json"
    )
    return {
        "bucket": bucket.name,
        "object_name": blob.name,
        "provider": "Google Cloud Storage",
    }
