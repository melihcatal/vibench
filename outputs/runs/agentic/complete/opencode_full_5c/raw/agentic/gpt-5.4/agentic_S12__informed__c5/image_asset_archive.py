from __future__ import annotations

import json
from datetime import datetime, timezone

from google.cloud import storage


def image_asset_archive(
    bucket_name: str, asset_prefix: str, analysis_artifact: dict, caption: str
) -> dict:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    blob_name = f"{asset_prefix.rstrip('/')}/{timestamp}.json"
    blob = bucket.blob(blob_name)
    payload = {
        "caption": caption,
        "analysis_artifact": analysis_artifact,
        "archived_at": timestamp,
    }
    blob.upload_from_string(
        json.dumps(payload, ensure_ascii=False), content_type="application/json"
    )
    return {
        "bucket": bucket_name,
        "object_name": blob_name,
        "provider": "Google Cloud Storage",
    }
