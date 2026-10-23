from google.cloud import storage
import os
import json
import datetime

def image_asset_archive(image_bytes: bytes, analysis_artifacts: dict, config: dict = None) -> dict:
    config = config or {}
    
    bucket_name = os.environ.get("GCS_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME environment variable not set.")

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # Generate a unique filename for the image and artifacts
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    image_blob_name = f"images/{timestamp}_image.jpg"
    artifacts_blob_name = f"artifacts/{timestamp}_analysis.json"

    # Upload image bytes
    image_blob = bucket.blob(image_blob_name)
    image_blob.upload_from_string(image_bytes, content_type="image/jpeg")
    image_public_url = image_blob.public_url

    # Upload analysis artifacts as a JSON file
    artifacts_json = json.dumps(analysis_artifacts, indent=2)
    artifacts_blob = bucket.blob(artifacts_blob_name)
    artifacts_blob.upload_from_string(artifacts_json, content_type="application/json")
    artifacts_public_url = artifacts_blob.public_url

    return {
        "image_archive_url": image_public_url,
        "artifacts_archive_url": artifacts_public_url,
        "bucket_name": bucket_name
    }
