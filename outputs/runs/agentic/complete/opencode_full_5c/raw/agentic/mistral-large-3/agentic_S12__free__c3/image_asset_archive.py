import os
from google.cloud import storage
from typing import Dict
from datetime import datetime
from .vision_models import ArchiveRequest


def archive_image_asset(request: ArchiveRequest) -> Dict:
    """Archives image-analysis artifacts and derived captions in Google Cloud Storage."""
    storage_client = storage.Client()
    bucket_name = os.getenv("GCS_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME environment variable not set.")

    bucket = storage_client.bucket(bucket_name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Upload image
    image_blob = bucket.blob(
        f"images/{timestamp}_{os.path.basename(request.image_path)}"
    )
    image_blob.upload_from_filename(request.image_path)

    # Upload analysis results
    results_blob = bucket.blob(f"analysis/{timestamp}_results.json")
    results_blob.upload_from_string(str(request.analysis_results))

    return {
        "provider": "google_cloud_storage",
        "image_uri": image_blob.public_url,
        "results_uri": results_blob.public_url,
        "timestamp": timestamp,
    }
