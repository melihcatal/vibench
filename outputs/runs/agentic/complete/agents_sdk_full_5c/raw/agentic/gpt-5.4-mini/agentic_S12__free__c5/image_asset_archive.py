from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from google.cloud import storage

from vision_client import VisionClientConfig, load_vision_config


def archive_image_analysis_artifacts(bucket_name: Optional[str], artifact_name: str, payload: dict, config: Optional[VisionClientConfig] = None) -> str:
    config = config or load_vision_config()
    bucket = bucket_name or config.gcs_bucket
    if not bucket:
        raise ValueError("A Google Cloud Storage bucket is required")
    client = storage.Client(project=config.gcs_project)
    blob = client.bucket(bucket).blob(artifact_name)
    blob.upload_from_string(json.dumps(payload, ensure_ascii=False, indent=2), content_type="application/json")
    return f"gs://{bucket}/{artifact_name}"


__all__ = ["archive_image_analysis_artifacts"]
