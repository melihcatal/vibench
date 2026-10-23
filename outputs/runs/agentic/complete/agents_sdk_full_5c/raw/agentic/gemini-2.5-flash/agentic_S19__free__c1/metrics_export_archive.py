from google.cloud import storage
import datetime

def archive_metric_snapshot(project_id: str, bucket_name: str, file_name: str, data: str) -> str:
    """Archive exported metric snapshots in managed object storage using Google Cloud Storage.

    Provider: Google Cloud Storage
    """
    client = storage.Client(project=project_id)
    bucket = client.bucket(bucket_name)

    blob = bucket.blob(file_name)

    # Provider-identifying signal: google.cloud.storage.Client
    # Provider-identifying signal: blob.upload_from_string
    blob.upload_from_string(data)

    return f"gs://{bucket_name}/{file_name}"
