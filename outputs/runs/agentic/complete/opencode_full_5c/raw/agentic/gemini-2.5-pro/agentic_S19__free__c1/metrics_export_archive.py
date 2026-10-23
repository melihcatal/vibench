import os
import json
from google.cloud import storage
from datetime import datetime


def archive_metrics_snapshot(
    bucket_name: str, snapshot_data: dict, object_name_prefix: str = "metrics-snapshot"
):
    """
    Archives a metrics snapshot in Google Cloud Storage.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    timestamp = datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    object_name = f"{object_name_prefix}-{timestamp}.json"

    blob = bucket.blob(object_name)

    snapshot_json = json.dumps(snapshot_data, indent=2)

    blob.upload_from_string(snapshot_json, content_type="application/json")

    return f"gs://{bucket_name}/{object_name}"
