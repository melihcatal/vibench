from __future__ import annotations

import hashlib
import json
from typing import Any, Dict

from google.cloud import storage

from observability_models import ArchiveResult


def metrics_export_archive(snapshot: Dict[str, Any], bucket_name: str, object_name: str) -> ArchiveResult:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    payload = json.dumps(snapshot, separators=(",", ":"), sort_keys=True).encode("utf-8")
    blob.upload_from_string(payload, content_type="application/json")
    md5_hash = hashlib.md5(payload).hexdigest()
    return ArchiveResult(
        bucket=bucket_name,
        object_name=object_name,
        uri=f"gs://{bucket_name}/{object_name}",
        md5_hash=md5_hash,
    )
