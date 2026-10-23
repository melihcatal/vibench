import os
from google.cloud import storage

def archive_image_analysis_artifacts(bucket_name: str, file_name: str, data: bytes, content_type: str) -> str:
    """
    Archives image analysis artifacts and derived captions in Google Cloud Storage.

    Args:
        bucket_name: The name of the GCS bucket.
        file_name: The desired file name in GCS.
        data: The content of the file to upload (e.g., image bytes, JSON bytes).
        content_type: The MIME type of the content (e.g., 'image/jpeg', 'application/json').

    Returns:
        The public URL of the uploaded object.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    
    blob.upload_from_string(data, content_type=content_type)
    
    return blob.public_url
