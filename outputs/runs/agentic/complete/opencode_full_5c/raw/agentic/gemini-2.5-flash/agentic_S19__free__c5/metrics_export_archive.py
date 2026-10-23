import os
from observability_client import get_storage_client
from google.cloud import storage
import json


def archive_metric_snapshot(
    bucket_name: str,
    destination_blob_name: str,
    metric_data: dict,
):
    """Archive exported metric snapshots in managed object storage (Google Cloud Storage)."""
    client: storage.Client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Convert metric data to JSON string for storage
    json_data = json.dumps(metric_data, indent=2)

    blob.upload_from_string(json_data, content_type="application/json")

    return f"gs://{bucket_name}/{destination_blob_name}"
