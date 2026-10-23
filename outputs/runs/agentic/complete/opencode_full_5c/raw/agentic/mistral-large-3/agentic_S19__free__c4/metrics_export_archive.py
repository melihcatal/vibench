import os
from datetime import datetime
from typing import Dict, List
from google.cloud import storage
from observability_client import ObservabilityClient
from observability_models import MetricPoint


def export_metric_snapshot(
    metric_type: str, hours: int = 1, label_filters: Dict[str, str] = None
) -> List[MetricPoint]:
    """Export a snapshot of metric data using Google Cloud Monitoring."""
    client = ObservabilityClient()
    return query_metric_window(metric_type, hours, label_filters)


def archive_to_gcs(
    metric_points: List[MetricPoint], bucket_name: str, prefix: str = "metrics"
):
    """Archive exported metric snapshots in Google Cloud Storage."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    timestamp = datetime.utcnow().isoformat()
    blob = bucket.blob(f"{prefix}/{timestamp}.json")
    blob.upload_from_string(
        data=str(
            [
                {
                    "timestamp": p.timestamp.isoformat(),
                    "value": p.value,
                    "labels": p.labels,
                }
                for p in metric_points
            ]
        )
    )
    return blob.public_url


def metrics_export_archive(
    metric_type: str,
    bucket_name: str,
    hours: int = 1,
    label_filters: Dict[str, str] = None,
):
    """Archive exported metric snapshots in managed object storage."""
    snapshot = export_metric_snapshot(metric_type, hours, label_filters)
    return archive_to_gcs(snapshot, bucket_name)
