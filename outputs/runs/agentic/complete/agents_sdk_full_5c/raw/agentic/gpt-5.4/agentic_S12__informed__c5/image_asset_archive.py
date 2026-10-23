from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

from google.cloud import storage


PROVIDER = "google-cloud-storage"


def archive_image_artifacts(
    bucket_name: str,
    object_prefix: str,
    analysis_result: Dict[str, Any],
    caption_text: str,
    image_bytes: Optional[bytes] = None,
    image_content_type: str = "image/jpeg",
) -> dict:
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS is required for Google Cloud Storage")

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    uploaded = []

    analysis_blob = bucket.blob(f"{object_prefix}/analysis.json")
    analysis_blob.upload_from_string(
        json.dumps(analysis_result, ensure_ascii=False, indent=2),
        content_type="application/json",
    )
    uploaded.append(analysis_blob.name)

    caption_blob = bucket.blob(f"{object_prefix}/caption.txt")
    caption_blob.upload_from_string(caption_text, content_type="text/plain; charset=utf-8")
    uploaded.append(caption_blob.name)

    if image_bytes is not None:
        image_blob = bucket.blob(f"{object_prefix}/image")
        image_blob.upload_from_string(image_bytes, content_type=image_content_type)
        uploaded.append(image_blob.name)

    return {
        "provider": PROVIDER,
        "bucket": bucket_name,
        "objects": uploaded,
        "storage_url_prefix": f"gs://{bucket_name}/{object_prefix}",
    }
