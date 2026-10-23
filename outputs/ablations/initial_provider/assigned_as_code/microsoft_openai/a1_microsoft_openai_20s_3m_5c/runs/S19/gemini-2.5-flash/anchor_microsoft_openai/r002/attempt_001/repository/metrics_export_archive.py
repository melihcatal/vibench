import os
from google.cloud import storage
import json

def archive_metric_snapshot(snapshot_data: dict, bucket_name: str, destination_blob_name: str, config: dict = None) -> dict:
    config = config or {}
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Convert snapshot data to a JSON string
    snapshot_json = json.dumps(snapshot_data, indent=2)

    blob.upload_from_string(snapshot_json, content_type='application/json')

    return {'gcs_uri': f"gs://{bucket_name}/{destination_blob_name}"}
