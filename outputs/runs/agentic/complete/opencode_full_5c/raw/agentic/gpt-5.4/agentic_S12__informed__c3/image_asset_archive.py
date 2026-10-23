from __future__ import annotations

import json
from typing import Any, Dict

from google.cloud import storage

from vision_models import ArchiveResult


def archive_image_artifacts(
    bucket_name: str, object_name: str, artifacts: Dict[str, Any]
) -> dict:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_string(
        json.dumps(artifacts, ensure_ascii=False), content_type="application/json"
    )
    result = ArchiveResult(
        provider="google-cloud-storage",
        bucket=bucket_name,
        object_name=object_name,
        uri=f"gs://{bucket_name}/{object_name}",
    )
    return result.to_dict()
