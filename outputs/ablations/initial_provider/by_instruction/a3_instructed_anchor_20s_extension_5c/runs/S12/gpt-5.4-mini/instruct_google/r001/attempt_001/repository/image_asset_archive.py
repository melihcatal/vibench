import os

from google.cloud import storage


def image_asset_archive(bucket_name: str, object_name: str, content: bytes):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_string(content)
    return f"gs://{bucket_name}/{object_name}"
