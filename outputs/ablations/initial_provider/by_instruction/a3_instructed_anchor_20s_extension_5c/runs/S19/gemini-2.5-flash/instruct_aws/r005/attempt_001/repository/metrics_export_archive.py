from google.cloud import storage
from datetime import datetime
import json

def archive_metric_snapshot(bucket_name: str, snapshot_data: dict, file_prefix: str = "metrics_snapshot") -> dict:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{file_prefix}_{timestamp}.json"
    blob = bucket.blob(file_name)

    # Upload the JSON data as a string
    blob.upload_from_string(json.dumps(snapshot_data), content_type="application/json")

    return {
        "bucket_name": bucket_name,
        "file_name": file_name,
        "public_url": blob.public_url,
        "message": f"Metric snapshot archived successfully to gs://{bucket_name}/{file_name}"
    }
