from __future__ import annotations

import json
from typing import Any, Dict

from google.cloud import storage

GCS_PROVIDER = "google-cloud-storage"


def image_asset_archive(bucket_name: str, object_prefix: str, artifacts: Dict[str, Any]) -> Dict[str, Any]:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    uploaded = []
    for name, payload in artifacts.items():
        blob_name = f"{object_prefix.rstrip('/')}/{name}.json"
        blob = bucket.blob(blob_name)
        blob.upload_from_string(json.dumps(payload, ensure_ascii=False, indent=2), content_type="application/json")
        uploaded.append({
            "name": name,
            "blob_name": blob_name,
            "gs_uri": f"gs://{bucket_name}/{blob_name}",
        })
    return {
        "provider": GCS_PROVIDER,
        "bucket": bucket_name,
        "uploaded": uploaded,
    }
