from google.cloud import storage
import datetime
from typing import Dict, Any

def archive_metric_snapshot(project_id: str, bucket_name: str, file_name_prefix: str, snapshot_data: str) -> str:
    client = storage.Client(project=project_id)
    bucket = client.bucket(bucket_name)

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    blob_name = f"{file_name_prefix}-{timestamp}.json"

    blob = bucket.blob(blob_name)
    blob.upload_from_string(snapshot_data, content_type="application/json")

    return f"gs://{bucket_name}/{blob_name}"