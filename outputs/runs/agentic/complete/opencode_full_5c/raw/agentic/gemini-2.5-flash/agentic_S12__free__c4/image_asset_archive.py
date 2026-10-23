from google.cloud import storage
import os


def archive_image_asset(bucket_name, destination_blob_name, data):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data)

    return blob.public_url
