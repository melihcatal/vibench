import os
from google.cloud import storage
from typing import Dict, Any


def archive_image_analysis_artifacts(
    bucket_name: str, file_name: str, data: bytes, content_type: str
) -> str:
    """
    Archives image analysis artifacts and derived captions in Google Cloud Storage.
    The GOOGLE_APPLICATION_CREDENTIALS environment variable must be set
    or credentials must be configured in the environment.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    blob.upload_from_string(data, content_type=content_type)

    return blob.public_url
