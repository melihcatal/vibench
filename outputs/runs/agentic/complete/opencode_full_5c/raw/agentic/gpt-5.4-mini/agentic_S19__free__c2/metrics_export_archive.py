import os

from google.cloud import storage


def metrics_export_archive(bucket_name, source_path, destination_blob_name=None):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob_name = destination_blob_name or os.path.basename(source_path)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(source_path)
    return {"bucket": bucket_name, "object": blob_name}
