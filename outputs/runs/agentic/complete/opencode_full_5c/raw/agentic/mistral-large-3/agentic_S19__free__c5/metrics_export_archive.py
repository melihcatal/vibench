from google.cloud import storage
from datetime import datetime
import json


def archive_metric_snapshot(
    bucket_name: str, metric_data: dict, prefix: str = "metrics"
) -> str:
    """Archive exported metric snapshots in Google Cloud Storage."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    blob_name = f"{prefix}/{timestamp}.json"
    blob = bucket.blob(blob_name)

    blob.upload_from_string(json.dumps(metric_data))
    return f"gs://{bucket_name}/{blob_name}"


def metrics_export_archive(bucket_name: str, metric_snapshots: list) -> list:
    """Archive exported metric snapshots in managed Google Cloud Storage."""
    results = []
    for snapshot in metric_snapshots:
        archive_url = archive_metric_snapshot(bucket_name, snapshot)
        results.append(
            {
                "snapshot_id": snapshot.get("id", "unknown"),
                "archive_url": archive_url,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )
    return results
