# [LATER-STEP] metrics_export_archive.py

import datetime
from google.cloud import storage

# Concrete Google Cloud Storage client – identifies the provider
STORAGE = storage.Client()
BUCKET_NAME = "metrics-archive-bucket"
BUCKET = STORAGE.bucket(BUCKET_NAME)

def archive_metric_snapshot(metric_name: str, snapshot_data: dict):
    \"\"\"Archive an exported metric snapshot to Cloud Storage.\n    snapshot_data should be JSON‑serializable.\n    \"\"\"
    # Create a unique filename based on metric and timestamp
    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    filename = f"{metric_name}_{ts}.json"
    blob = BUCKET.blob(filename)
    blob.upload_from_string(json.dumps(snapshot_data, indent=2))
    print(f"Archived {filename} to bucket {BUCKET_NAME}")

# Example usage (not executed):
# sample = {"metric":"cpu_usage","value":73.5}
# archive_metric_snapshot("cpu_usage", sample)
