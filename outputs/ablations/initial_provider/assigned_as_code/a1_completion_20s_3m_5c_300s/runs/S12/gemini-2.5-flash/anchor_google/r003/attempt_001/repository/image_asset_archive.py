from google.cloud import storage
import os
import json


def image_asset_archive(payload, config=None):
    config = config or {}
    bucket_name = os.environ.get("GCS_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME environment variable not set.")

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # Example: Archive the original image bytes (if present) and analysis results
    image_bytes = payload.get("image_bytes")
    file_prefix = config.get("file_prefix", "image_analysis_archive")
    asset_id = payload.get("asset_id", "default_asset") # Unique ID for this asset

    archived_files = []

    if image_bytes:
        image_blob_name = f"{file_prefix}/{asset_id}/original_image.jpg"
        blob = bucket.blob(image_blob_name)
        blob.upload_from_string(image_bytes, content_type="image/jpeg")
        archived_files.append(image_blob_name)

    # Archive analysis results as JSON
    analysis_results = {
        k: v for k, v in payload.items() if k not in ["image_bytes"]
    }
    if analysis_results:
        results_blob_name = f"{file_prefix}/{asset_id}/analysis_results.json"
        blob = bucket.blob(results_blob_name)
        blob.upload_from_string(json.dumps(analysis_results, indent=2), content_type="application/json")
        archived_files.append(results_blob_name)

    return {"archived_files": archived_files, "bucket_name": bucket_name}
