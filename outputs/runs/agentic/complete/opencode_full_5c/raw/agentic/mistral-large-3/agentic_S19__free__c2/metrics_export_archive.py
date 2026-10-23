from google.cloud import storage
from datetime import datetime
import json
from typing import Dict, List
from observability_client import ObservabilityClient
from query_metric_window import query_metric_window


def archive_metrics_export(metric_name: str, bucket_name: str, hours: int = 1) -> str:
    client = ObservabilityClient()
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    metric_data = query_metric_window(metric_name, hours)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"metrics/{metric_name}_{timestamp}.json"
    blob = bucket.blob(filename)

    export_data = {
        "metric_type": metric_data.metric_type,
        "points": [
            {"value": p.value, "timestamp": p.timestamp.isoformat(), "labels": p.labels}
            for p in metric_data.points
        ],
    }

    blob.upload_from_string(json.dumps(export_data))
    return f"gs://{bucket_name}/{filename}"
