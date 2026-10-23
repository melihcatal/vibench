import os
import json
from google.cloud import storage

def archive_image_assets(image_id: str, analysis_report: str, bucket_name: str = "my-image-assets"):
    """Archive image-analysis artifacts and derived captions in Google Cloud Storage."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob_name = f"images/{image_id}/report.json"
    blob = bucket.blob(blob_name)
    blob.upload_from_string(analysis_report, content_type="application/json")
    print(f"Archived report to gs://{bucket_name}/{blob_name}")
