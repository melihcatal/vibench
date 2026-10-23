from google.cloud import storage
import os

def get_storage_client():
    return storage.Client()

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
