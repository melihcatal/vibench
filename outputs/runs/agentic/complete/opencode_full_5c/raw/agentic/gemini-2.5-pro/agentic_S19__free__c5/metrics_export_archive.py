import os
import json
from datetime import datetime

from observability_client import get_storage_client


def archive_metrics_snapshot(
    bucket_name: str, snapshot_data: dict, file_name: str = None
):
    """
    Uploads a metric snapshot (as a JSON string) to a Google Cloud Storage bucket.
    """
    storage_client = get_storage_client()
    bucket = storage_client.bucket(bucket_name)

    if not file_name:
        timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        file_name = f"metric-snapshot-{timestamp}.json"

    blob = bucket.blob(file_name)

    # Convert dict to JSON string for upload
    snapshot_json = json.dumps(snapshot_data, indent=2)

    blob.upload_from_string(snapshot_json, content_type="application/json")

    print(f"Successfully uploaded snapshot to gs://{bucket_name}/{file_name}")
    return f"gs://{bucket_name}/{file_name}"


if __name__ == "__main__":
    gcs_bucket = os.environ.get("GCS_BUCKET_NAME")
    if not gcs_bucket:
        raise ValueError("GCS_BUCKET_NAME environment variable must be set")

    # Example snapshot data
    mock_snapshot = {
        "metadata": {
            "source": "metrics-exporter-v1",
            "timestamp_utc": datetime.utcnow().isoformat(),
            "metrics_included": 2,
        },
        "metrics": [
            {
                "name": "compute.googleapis.com/instance/cpu/utilization",
                "resource_filter": "resource.labels.zone = 'us-central1-a'",
                "aggregated_value": 0.55,
                "time_window_minutes": 60,
            },
            {
                "name": "custom.googleapis.com/transaction_volume",
                "resource_filter": "metric.labels.status = 'success'",
                "aggregated_value": 15032,
                "time_window_minutes": 60,
            },
        ],
    }

    archive_metrics_snapshot(gcs_bucket, mock_snapshot)
