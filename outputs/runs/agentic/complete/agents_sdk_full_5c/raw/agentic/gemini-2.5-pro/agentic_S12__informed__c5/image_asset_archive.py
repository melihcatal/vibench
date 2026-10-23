"""
[LATER-STEP] image_asset_archive.py - Archive image-analysis artifacts and derived captions in managed object storage
"""

import os
import json
from google.cloud import storage
from vision_models import VisionResult

def archive_assets(
    image_path: str,
    analysis_results: VisionResult,
    bucket_name: str,
    prefix: str = "image-analysis/"
):
    """
    Uploads the original image and its analysis results to Google Cloud Storage.
    
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set in the environment.
    """
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
    except Exception as e:
        print(f"Failed to initialize Google Cloud Storage client: {e}")
        print("Please ensure GOOGLE_APPLICATION_CREDENTIALS is set correctly.")
        return

    base_filename = os.path.basename(image_path)
    
    # Upload the original image
    image_blob_name = f"{prefix}{base_filename}"
    image_blob = bucket.blob(image_blob_name)
    image_blob.upload_from_filename(image_path)
    print(f"Uploaded image to gs://{bucket_name}/{image_blob_name}")

    # Upload the analysis results as a JSON file
    results_json = analysis_results.model_dump_json(indent=2)
    json_blob_name = f"{prefix}{base_filename}.json"
    json_blob = bucket.blob(json_blob_name)
    json_blob.upload_from_string(results_json, content_type='application/json')
    print(f"Uploaded analysis results to gs://{bucket_name}/{json_blob_name}")
