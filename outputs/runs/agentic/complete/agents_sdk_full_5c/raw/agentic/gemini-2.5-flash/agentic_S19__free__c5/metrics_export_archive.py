from google.cloud import storage
import json
import datetime

def archive_metrics_snapshot(bucket_name: str, file_prefix: str, metrics_data: list, project_id: str):
    client = storage.Client(project=project_id) # Provider-identifying signal: storage.Client
    bucket = client.get_bucket(bucket_name)

    timestamp = datetime.datetime.now().isoformat()
    file_name = f"{file_prefix}_{timestamp}.json"
    blob = bucket.blob(file_name)

    data_to_upload = json.dumps(metrics_data, indent=2)

    blob.upload_from_string(data_to_upload, content_type="application/json")

    return {
        "bucket": bucket_name,
        "file_name": file_name,
        "gcs_uri": f"gs://{bucket_name}/{file_name}",
        "uploaded_at": timestamp
    }
