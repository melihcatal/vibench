import os
import json
from google.cloud import storage

def archive_metrics_snapshot(metrics_data: dict, bucket_name: str, object_path: str) -> None:
    client = storage.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_path)
    blob.upload_from_string(json.dumps(metrics_data), content_type="application/json")
    blob.make_public()  # optional