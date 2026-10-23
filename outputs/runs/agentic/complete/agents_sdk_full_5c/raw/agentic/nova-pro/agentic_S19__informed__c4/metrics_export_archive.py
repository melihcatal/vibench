import os
from google.cloud import storage

def archive_metric_snapshot(bucket_name, source_file_name, destination_blob_name):
    client = storage.Client(credentials=os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)