import os
from google.cloud import storage


def archive_image_analysis_artifacts(
    bucket_name: str,
    file_name: str,
    data: bytes,
    content_type: str = "application/json",
) -> str:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    blob.upload_from_string(data, content_type=content_type)

    return blob.public_url
