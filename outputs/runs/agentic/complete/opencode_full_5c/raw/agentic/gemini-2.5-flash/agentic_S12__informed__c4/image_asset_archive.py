import os
from google.cloud import storage  # Provider-identifying signal


def archive_image_asset(
    file_content: bytes, destination_blob_name: str, bucket_name: str
) -> str:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(file_content)

    return f"gs://{bucket_name}/{destination_blob_name}"
