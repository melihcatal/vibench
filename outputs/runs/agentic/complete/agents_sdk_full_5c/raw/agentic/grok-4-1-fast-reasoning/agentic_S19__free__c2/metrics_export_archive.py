import json
import os
from typing import Any, Dict
from google.cloud import storage

def metrics_export_archive(metrics_snapshot: Dict[str, Any], bucket_name: str, blob_name: str) -> None:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    client = storage.Client(project=project_id)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(
        data=json.dumps(metrics_snapshot, indent=2),
        content_type="application/json"
    )
