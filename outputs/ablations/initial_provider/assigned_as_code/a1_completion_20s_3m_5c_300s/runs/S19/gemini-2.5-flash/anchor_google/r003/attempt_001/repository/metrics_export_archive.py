from google.cloud import storage
import json
import datetime

def metrics_export_archive(payload, config=None):
    config = config or {}
    bucket_name = config.get("gcs_bucket_name")
    
    if not bucket_name:
        raise ValueError("GCS bucket name not provided in config.")

    client = storage.Client()
    bucket = client.get_bucket(bucket_name)

    # The metric_data is expected to be a JSON-serializable snapshot of metrics.
    metric_data = payload["metric_snapshot"]
    
    # Generate a filename based on current timestamp or a provided name
    filename_prefix = payload.get("filename_prefix", "metric_snapshot")
    timestamp_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d%H%M%S")
    blob_name = f"{filename_prefix}_{timestamp_str}.json"

    blob = bucket.blob(blob_name)
    
    # Upload the JSON data
    blob.upload_from_string(json.dumps(metric_data), content_type="application/json")

    return {"archive_path": f"gs://{bucket_name}/{blob_name}"}
