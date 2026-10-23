from typing import Dict

from google.cloud import storage


def metrics_export_archive(bucket_name: str, blob_name: str, content: bytes, content_type: str = "application/json") -> Dict[str, str]:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(content, content_type=content_type)
    return {"bucket": bucket_name, "blob": blob_name, "gcs_uri": f"gs://{bucket_name}/{blob_name}"}
