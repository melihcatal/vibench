import json
import os
from typing import Any, Dict, Optional

from google.cloud import storage

GCS_BUCKET_ENV = "GCS_BUCKET_NAME"


def image_asset_archive(artifact_name: str, payload: Dict[str, Any], bucket_name: Optional[str] = None) -> str:
    bucket_name = bucket_name or os.getenv(GCS_BUCKET_ENV)
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME is required")
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(artifact_name)
    blob.upload_from_string(json.dumps(payload, ensure_ascii=False, indent=2), content_type="application/json")
    return f"gs://{bucket_name}/{artifact_name}"