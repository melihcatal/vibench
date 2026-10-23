from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict

from google.cloud import storage

from observability_models import ArchiveResult


GCS_PROVIDER = "Google Cloud Storage"


def metrics_export_archive(bucket_name: str, export_payload: Dict[str, Any], object_prefix: str = "metrics-exports") -> Dict[str, Any]:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    object_name = f"{object_prefix}/snapshot-{stamp}.json"
    blob = bucket.blob(object_name)
    blob.upload_from_string(json.dumps(export_payload, separators=(",", ":")), content_type="application/json")
    result = ArchiveResult(bucket=bucket_name, object_name=object_name, generation=str(blob.generation) if blob.generation is not None else None, uri=f"gs://{bucket_name}/{object_name}")
    return result.__dict__
