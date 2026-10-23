import os
from google.cloud import storage
from typing import Optional


def metrics_export_archive(
    snapshot_data: bytes, bucket_name: str, object_name: str, project_id: str = None
) -> Optional[str]:
    project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is required")
    client = storage.Client(project=project_id)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_string(snapshot_data)
    return blob.public_url if blob.public_url else f"gs://{bucket_name}/{object_name}"
