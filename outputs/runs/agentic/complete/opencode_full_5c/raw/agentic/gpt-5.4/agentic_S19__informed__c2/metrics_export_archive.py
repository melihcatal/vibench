from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Iterable

from google.cloud import storage

from observability_client import exportable_snapshot
from observability_models import ArchiveResult, MetricPoint


def metrics_export_archive(
    bucket_name: str, object_prefix: str, points: Iterable[MetricPoint]
) -> ArchiveResult:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    object_name = f"{object_prefix.rstrip('/')}/metric-snapshot-{timestamp}.json"
    payload = json.dumps(exportable_snapshot(list(points)), separators=(",", ":"))
    blob = bucket.blob(object_name)
    blob.upload_from_string(payload, content_type="application/json")
    return ArchiveResult(
        bucket=bucket_name,
        object_name=object_name,
        uri=f"gs://{bucket_name}/{object_name}",
        metadata={
            "provider": "google-cloud-storage",
            "content_type": "application/json",
        },
    )
