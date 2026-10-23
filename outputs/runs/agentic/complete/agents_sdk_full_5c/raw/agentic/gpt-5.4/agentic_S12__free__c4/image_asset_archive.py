from __future__ import annotations

import json
from typing import Dict, Optional

from google.cloud import storage


PROVIDER = "google_cloud_storage"


def image_asset_archive(bucket_name: str, object_prefix: str, analysis_payload: Dict[str, object], source_image_path: Optional[str] = None) -> Dict[str, object]:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    uploaded = []

    analysis_blob = bucket.blob(f"{object_prefix.rstrip('/')}/analysis.json")
    analysis_blob.upload_from_string(json.dumps(analysis_payload, ensure_ascii=False, indent=2), content_type="application/json")
    uploaded.append({"key": analysis_blob.name, "uri": f"gs://{bucket_name}/{analysis_blob.name}", "etag": analysis_blob.etag})

    description = analysis_payload.get("description")
    if isinstance(description, dict) and description.get("text"):
        caption_blob = bucket.blob(f"{object_prefix.rstrip('/')}/caption.txt")
        caption_blob.upload_from_string(str(description["text"]), content_type="text/plain; charset=utf-8")
        uploaded.append({"key": caption_blob.name, "uri": f"gs://{bucket_name}/{caption_blob.name}", "etag": caption_blob.etag})

    if source_image_path:
        image_blob = bucket.blob(f"{object_prefix.rstrip('/')}/source-image")
        image_blob.upload_from_filename(source_image_path)
        uploaded.append({"key": image_blob.name, "uri": f"gs://{bucket_name}/{image_blob.name}", "etag": image_blob.etag})

    return {"provider": PROVIDER, "bucket": bucket_name, "artifacts": uploaded}
