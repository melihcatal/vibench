import json
import datetime

from google.cloud import storage

def archive_metric_snapshot(snapshot_data: dict, bucket_name: str, config=None):
    config = config or {}
    storage_client = storage.Client(project=config["project_id"])
    bucket = storage_client.bucket(bucket_name)

    timestamp = datetime.datetime.now().isoformat()
    blob_name = f"metric_snapshots/{snapshot_data.get("metric_name", "unknown")}-{timestamp}.json"

    blob = bucket.blob(blob_name)
    blob.upload_from_string(json.dumps(snapshot_data, indent=2), content_type="application/json")

    return {"archive_path": f"gs://{bucket_name}/{blob_name}"}
