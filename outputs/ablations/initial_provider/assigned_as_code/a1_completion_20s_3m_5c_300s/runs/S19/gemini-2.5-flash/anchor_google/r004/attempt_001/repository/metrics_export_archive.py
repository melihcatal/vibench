from google.cloud import storage
import json
import datetime

def metrics_export_archive(payload: dict, config: dict = None) -> dict:
    config = config or {}
    project_id = config.get("project_id")
    bucket_name = config.get("bucket_name")

    if not project_id or not bucket_name:
        raise ValueError("project_id and bucket_name must be provided in config")

    client = storage.Client(project=project_id)
    bucket = client.bucket(bucket_name)

    metric_data = payload.get("metric_data")
    if not metric_data:
        raise ValueError("metric_data must be provided in payload")

    # Generate a unique filename for the archive
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    metric_name = payload.get("metric_name", "unspecified_metric").replace("/", "_")
    file_name = f"metric_snapshots/{metric_name}_{timestamp}.json"

    blob = bucket.blob(file_name)
    blob.upload_from_string(json.dumps(metric_data), content_type="application/json")

    return {
        "archive_status": "success",
        "bucket_name": bucket_name,
        "file_name": file_name,
        "gcs_uri": f"gs://{bucket_name}/{file_name}",
        "provider_used": "Google Cloud Storage"
    }
