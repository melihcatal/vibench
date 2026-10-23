import os
from google.cloud import storage
from typing import Dict, Optional
from .vision_client import get_storage_client
from .vision_models import ImageAssetArchiveRequest


def archive_image_asset(request: ImageAssetArchiveRequest) -> str:
    """Archives image-analysis artifacts and derived captions in Google Cloud Storage."""
    storage_client = get_storage_client()
    if not storage_client:
        raise ValueError(
            "Google Cloud Storage client not initialized. Check credentials."
        )

    bucket_name = request.bucket_name or os.getenv("GCS_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("No bucket name provided or found in environment variables.")

    bucket = storage_client.bucket(bucket_name)

    # Upload the original image
    image_blob = bucket.blob(f"images/{os.path.basename(request.image_path)}")
    image_blob.upload_from_filename(request.image_path)

    # Upload analysis results
    results_blob = bucket.blob(f"analysis/{os.path.basename(request.image_path)}.json")
    results_blob.upload_from_string(str(request.analysis_results))

    return f"gs://{bucket_name}/{image_blob.name}"
