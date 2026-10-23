import os
from typing import Any, Dict, Iterable, List

from google.cloud import storage

from vision_client import load_vision_config


def image_asset_archive(bucket_name: str, artifacts: Dict[str, Any], prefix: str = "image-analysis") -> Dict[str, Any]:
    cfg = load_vision_config()
    client = storage.Client(project=cfg.get("project_id"))
    bucket = client.bucket(bucket_name)
    uploaded = []
    for name, payload in artifacts.items():
        blob = bucket.blob(f"{prefix}/{name}.json")
        blob.upload_from_string(str(payload), content_type="application/json")
        uploaded.append(blob.name)
    return {"provider": "google_cloud_storage", "bucket": bucket_name, "objects": uploaded}
