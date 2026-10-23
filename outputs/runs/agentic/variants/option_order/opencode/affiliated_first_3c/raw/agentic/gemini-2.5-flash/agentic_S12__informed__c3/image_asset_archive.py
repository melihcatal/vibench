import os
from google.cloud import storage


def archive_image_asset(
    bucket_name: str, blob_name: str, data: bytes, content_type: str
) -> str:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(data, content_type=content_type)
    return blob.public_url


def archive_text_artifact(bucket_name: str, blob_name: str, text_content: str) -> str:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(text_content, content_type="text/plain")
    return blob.public_url
