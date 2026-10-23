from google.cloud import storage
import os
from typing import Dict

def archive_image_analysis_artifacts(
    image_bytes: bytes,
    metadata: Dict[str, str],
    destination_blob_name: str
) -> str:
    client = storage.Client()
    bucket_name = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    
    blob.upload_from_string(image_bytes, content_type="image/jpeg")
    blob.metadata = metadata
    blob.patch()
    
    return f"gs://{bucket_name}/{destination_blob_name}"