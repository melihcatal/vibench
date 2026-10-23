import os
from datetime import datetime
from google.cloud import storage
from observability_client import get_client_config
import json


def archive_metrics_export(export_data: dict, bucket_name: str, object_prefix: str) -> str:
    """Archive exported metric snapshots in Google Cloud Storage."""
    client_config = get_client_config()
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    timestamp = datetime.utcnow().isoformat()
    object_name = f"{object_prefix}/metrics_export_{timestamp}.json"
    blob = bucket.blob(object_name)

    blob.upload_from_string(json.dumps(export_data))
    return f"gs://{bucket_name}/{object_name}"