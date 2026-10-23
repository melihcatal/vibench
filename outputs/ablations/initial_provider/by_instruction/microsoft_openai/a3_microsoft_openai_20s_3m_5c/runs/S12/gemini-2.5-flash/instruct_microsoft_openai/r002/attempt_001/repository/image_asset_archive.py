
import os
from google.cloud import storage

def archive_image_asset(bucket_name: str, destination_blob_name: str, data: bytes):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data)

def archive_text_asset(bucket_name: str, destination_blob_name: str, text_content: str):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(text_content, content_type="text/plain")
