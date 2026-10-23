from __future__ import annotations

import json
import os
from typing import Any, Dict

from google.cloud import storage


PROVIDER = "Google Cloud Storage"


def archive_image_artifacts(bucket_name: str, object_prefix: str, artifacts: Dict[str, Any]) -> dict:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    uploaded = []

    for name, payload in artifacts.items():
        blob = bucket.blob(f"{object_prefix.rstrip('/')}/{name}.json")
        blob.upload_from_string(
            json.dumps(payload, ensure_ascii=False, indent=2),
            content_type="application/json",
        )
        uploaded.append({"name": name, "gs_uri": f"gs://{bucket_name}/{blob.name}"})

    caption = artifacts.get("caption") or artifacts.get("description")
    if isinstance(caption, str):
        blob = bucket.blob(f"{object_prefix.rstrip('/')}/caption.txt")
        blob.upload_from_string(caption, content_type="text/plain; charset=utf-8")
        uploaded.append({"name": "caption", "gs_uri": f"gs://{bucket_name}/{blob.name}"})

    return {
        "provider": PROVIDER,
        "model": "google-cloud-storage-json-archive",
        "bucket": bucket_name,
        "GOOGLE_APPLICATION_CREDENTIALS": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        "uploaded": uploaded,
    }
