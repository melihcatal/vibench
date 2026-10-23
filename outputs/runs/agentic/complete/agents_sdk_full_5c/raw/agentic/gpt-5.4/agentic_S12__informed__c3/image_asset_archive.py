from __future__ import annotations

import json
from typing import Any, Dict, Optional

from google.cloud import storage

from vision_models import ArchiveArtifact


GCS_PROVIDER = "google-cloud-storage"


def archive_image_analysis_artifacts(
    bucket_name: str,
    object_prefix: str,
    analysis: Dict[str, Any],
    caption: str,
    content_type: Optional[str] = "application/json",
) -> Dict[str, ArchiveArtifact]:
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    analysis_blob = bucket.blob(f"{object_prefix.rstrip('/')}/analysis.json")
    analysis_blob.upload_from_string(json.dumps(analysis, ensure_ascii=False, indent=2), content_type=content_type)

    caption_blob = bucket.blob(f"{object_prefix.rstrip('/')}/caption.txt")
    caption_blob.upload_from_string(caption, content_type="text/plain; charset=utf-8")

    return {
        "analysis": ArchiveArtifact(
            key=analysis_blob.name,
            bucket=bucket_name,
            etag=analysis_blob.etag,
            url=f"gs://{bucket_name}/{analysis_blob.name}",
        ),
        "caption": ArchiveArtifact(
            key=caption_blob.name,
            bucket=bucket_name,
            etag=caption_blob.etag,
            url=f"gs://{bucket_name}/{caption_blob.name}",
        ),
    }
