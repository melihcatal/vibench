from google.cloud import storage
import os
from datetime import datetime
from typing import Dict, Any
import json

def archive_image_analysis_artifacts(
    image_bytes: bytes,
    analysis_results: Dict[str, Any],
    bucket_name: str,
    prefix: str = "image-analysis-archives/",
) -> Dict[str, str]:
    """
    Archives original image and its analysis results to Google Cloud Storage.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = os.urandom(8).hex() # To ensure unique filenames

    # Archive the original image
    image_blob_name = f"{prefix}{timestamp}-{unique_id}/original_image.jpg"
    image_blob = bucket.blob(image_blob_name)
    image_blob.upload_from_string(image_bytes, content_type="image/jpeg")

    # Archive the analysis results (as JSON)
    results_blob_name = f"{prefix}{timestamp}-{unique_id}/analysis_results.json"
    results_blob = bucket.blob(results_blob_name)
    results_blob.upload_from_string(json.dumps(analysis_results, indent=2), content_type="application/json")

    return {
        "image_gcs_uri": f"gs://{bucket_name}/{image_blob_name}",
        "results_gcs_uri": f"gs://{bucket_name}/{results_blob_name}",
    }
