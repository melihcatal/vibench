import os
import json
from google.cloud import storage

def archive_metric_snapshot(bucket_name: str, destination_blob_name: str, metric_data: dict) -> str:
    """
    Archives exported metric snapshots in Google Cloud Storage.
    `metric_data` is expected to be a dictionary that can be serialized to JSON.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Convert dictionary to a JSON string for storage
    data_to_store = json.dumps(metric_data, indent=2)

    try:
        blob.upload_from_string(data_to_store, content_type="application/json")
        return f"Metric snapshot archived to gs://{bucket_name}/{destination_blob_name}"
    except Exception as e:
        return f"Error archiving metric snapshot: {e}"
