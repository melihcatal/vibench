from __future__ import annotations

from typing import Dict

from google.cloud import storage


def metrics_export_archive(bucket_name: str, local_path: str, blob_name: str) -> Dict[str, str]:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(local_path)
    return {"bucket": bucket_name, "blob": blob_name, "provider": "Cloud Storage"}
