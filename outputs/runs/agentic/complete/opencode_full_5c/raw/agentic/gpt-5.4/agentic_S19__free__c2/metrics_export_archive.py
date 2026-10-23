from __future__ import annotations

import json
import os
from datetime import datetime

from google.cloud import storage

from query_metric_window import query_metric_window


def metrics_export_archive(
    metric_type: str,
    start_time: datetime,
    end_time: datetime,
    bucket_name: str,
    object_name: str,
    project_id: str | None = None,
    resource_type: str | None = None,
    filter_clauses: list[str] | None = None,
) -> dict:
    snapshot = query_metric_window(
        metric_type=metric_type,
        start_time=start_time,
        end_time=end_time,
        project_id=project_id,
        resource_type=resource_type,
        filter_clauses=filter_clauses,
    )
    payload = {
        "provider": "Google Cloud Storage",
        "project_id": snapshot.project_id,
        "metric_type": snapshot.metric_type,
        "start_time": snapshot.start_time,
        "end_time": snapshot.end_time,
        "series": [
            {
                "series_name": s.series_name,
                "resource_type": s.resource_type,
                "resource_labels": s.resource_labels,
                "metric_labels": s.metric_labels,
                "points": [p.__dict__ for p in s.points],
            }
            for s in snapshot.series
        ],
    }
    storage_client = storage.Client(
        project=project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    )
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_string(
        json.dumps(payload, separators=(",", ":")), content_type="application/json"
    )
    return {
        "bucket": bucket_name,
        "object_name": object_name,
        "gcs_uri": f"gs://{bucket_name}/{object_name}",
        "size_bytes": len(json.dumps(payload).encode("utf-8")),
    }
