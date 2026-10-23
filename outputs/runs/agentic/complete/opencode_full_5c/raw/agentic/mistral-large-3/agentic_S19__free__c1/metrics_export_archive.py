from google.cloud import storage
from typing import List, Dict
import json
import datetime


def archive_metrics_export(
    bucket_name: str, metric_data: List[Dict], prefix: str = "metrics"
) -> str:
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    blob_name = f"{prefix}/export_{timestamp}.json"
    blob = bucket.blob(blob_name)

    blob.upload_from_string(json.dumps(metric_data), content_type="application/json")

    return f"gs://{bucket_name}/{blob_name}"
