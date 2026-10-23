from google.cloud import storage
from observability_client import get_observability_client
from datetime import datetime
import json
import os


def archive_metrics_export(data: dict, bucket_name: str, object_prefix: str = "metrics") -> str:
    """Archive exported metric snapshots in Google Cloud Storage."""
    client = get_observability_client(storage.Client)
    bucket = client.bucket(bucket_name)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    object_name = f"{object_prefix}/export_{timestamp}.json"
    blob = bucket.blob(object_name)

    blob.upload_from_string(
        data=json.dumps(data),
        content_type="application/json"
    )

    return f"gs://{bucket_name}/{object_name}"