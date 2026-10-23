from google.cloud import storage
import json
from datetime import datetime
from typing import Any

def metrics_export_archive(
    data: Any,
    bucket_name: str,
    prefix: str = "metrics/"
) -> str:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    timestamp = datetime.utcnow().isoformat().replace(":", "-").replace(".", "-")
    blob_name = f"{prefix}{timestamp}.json"
    blob = bucket.blob(blob_name)
    blob.upload_from_string(
        json.dumps(data, default=str),
        content_type="application/json"
    )
    return f"gs://{bucket_name}/{blob_name}"