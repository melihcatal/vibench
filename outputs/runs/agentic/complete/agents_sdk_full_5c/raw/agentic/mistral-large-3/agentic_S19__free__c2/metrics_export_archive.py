import os
from datetime import datetime
from google.cloud import storage
from observability_models import MetricDataPoint


def archive_metrics_export(data_points: list[MetricDataPoint], bucket_name: str, object_prefix: str = "metrics") -> str:
    """Archive exported metric snapshots in Google Cloud Storage."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    object_name = f"{object_prefix}/export_{timestamp}.json"
    blob = bucket.blob(object_name)

    export_data = [
        {
            "timestamp": point.timestamp,
            "value": point.value,
            "labels": point.labels,
        }
        for point in data_points
    ]

    import json
    blob.upload_from_string(json.dumps(export_data, indent=2))

    return f"gs://{bucket_name}/{object_name}"