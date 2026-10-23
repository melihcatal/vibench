import os
from google.cloud import storage
import json
from datetime import datetime


def archive_metric_snapshot(bucket_name: str, file_name: str, metrics_data: dict):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Ensure the metrics_data is JSON serializable
    data_to_save = json.dumps(metrics_data, indent=2)

    blob.upload_from_string(data_to_save, content_type="application/json")
    return f"gs://{bucket_name}/{file_name}"
