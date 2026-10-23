from __future__ import annotations

import json
import os
from typing import Any, Mapping

from google.cloud import storage


GCS_PROVIDER = "storage.googleapis.com"
GCS_BUCKET_ENV = "GCS_BUCKET_NAME"


def image_asset_archive(object_name: str, artifacts: Mapping[str, Any], bucket_name: str | None = None) -> str:
    client = storage.Client()
    bucket = client.bucket(bucket_name or os.environ[GCS_BUCKET_ENV])
    blob = bucket.blob(object_name)
    blob.upload_from_string(json.dumps(dict(artifacts), ensure_ascii=False, indent=2), content_type="application/json")
    return f"gs://{bucket.name}/{object_name}"
