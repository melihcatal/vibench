import os

from google.cloud import storage


def metrics_export_archive(bucket_name: str, source_path: str, destination_blob: str | None = None):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob or os.path.basename(source_path))
    blob.upload_from_filename(source_path)
    return {"bucket": bucket_name, "blob": blob.name}
