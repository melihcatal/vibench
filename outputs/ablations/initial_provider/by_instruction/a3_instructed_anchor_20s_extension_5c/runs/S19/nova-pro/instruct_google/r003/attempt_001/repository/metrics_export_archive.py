import google.auth
from google.cloud import storage

def archive_metric_snapshot(bucket_name, source_file_name, destination_blob_name):
    credentials, project = google.auth.default()
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)