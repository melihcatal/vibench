from google.cloud import storage
import os
from typing import Dict, Optional
from datetime import datetime


def image_asset_archive(
    image_path: str, analysis_results: Dict, destination_blob_name: Optional[str] = None
) -> str:
    """Archives image-analysis artifacts and derived captions in Google Cloud Storage."""
    client = storage.Client()
    bucket_name = os.getenv("GCS_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME environment variable not set.")

    bucket = client.bucket(bucket_name)

    if not destination_blob_name:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        destination_blob_name = f"image_analysis_{timestamp}.json"

    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(str(analysis_results))

    return f"gs://{bucket_name}/{destination_blob_name}"
