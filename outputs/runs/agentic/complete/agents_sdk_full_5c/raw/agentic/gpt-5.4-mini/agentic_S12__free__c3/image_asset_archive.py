from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from google.cloud import storage

BUCKET_ENV = "GOOGLE_CLOUD_STORAGE_BUCKET"


def image_asset_archive(bucket_name: str, artifact_name: str, payload: Dict[str, Any]) -> str:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(artifact_name)
    blob.upload_from_string(json.dumps(payload, ensure_ascii=False, indent=2), content_type="application/json")
    return f"gs://{bucket_name}/{artifact_name}"
