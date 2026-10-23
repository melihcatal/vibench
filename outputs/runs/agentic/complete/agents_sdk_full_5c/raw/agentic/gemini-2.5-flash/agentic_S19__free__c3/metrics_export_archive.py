from google.cloud import storage
import json
import datetime
import os

def archive_metrics_snapshot(bucket_name: str, snapshot_data: dict, filename_prefix: str = "metrics_snapshot"):
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Generate a unique filename using a timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    blob_name = f"{filename_prefix}_{timestamp}.json"

    blob = bucket.blob(blob_name)

    # Convert the snapshot data to a JSON string and upload
    json_data = json.dumps(snapshot_data, indent=2)
    blob.upload_from_string(json_data, content_type="application/json")

    return f"gs://{bucket_name}/{blob_name}"
