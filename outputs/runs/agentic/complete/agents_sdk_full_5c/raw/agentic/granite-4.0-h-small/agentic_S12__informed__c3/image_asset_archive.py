# image_asset_archive.py
import os
import io
from google.cloud import storage
from .image_summary import VisualAnalysis

# Google Cloud Storage credentials via GOOGLE_APPLICATION_CREDENTIALS env var
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
assert GCS_BUCKET_NAME, "Set GCS_BUCKET_NAME environment variable"

storage_client = storage.Client()
bucket = storage_client.bucket(GCS_BUCKET_NAME)


def archive_analysis(analysis: VisualAnalysis, image_name: str, metadata: dict = None):
    """Upload analysis results and optional image to a managed Google Cloud Storage bucket."""
    blob_prefix = f"visual_analysis/{image_name}/"
    # Save labels
    labels_blob = bucket.blob(f"{blob_prefix}labels.json")
    labels_blob.upload_from_string(analysis.labels or "[]", content_type="application/json")
    # Save description
    desc_blob = bucket.blob(f"{blob_prefix}description.txt")
    desc_blob.upload_from_string(analysis.description or "")
    # Save safety flags
    safety_blob = bucket.blob(f"{blob_prefix}safety.json")
    safety_blob.upload_from_string(str(analysis.safe), content_type="application/json")
    # Optionally store the original image
    if metadata and metadata.get("image_bytes"):
        img_blob = bucket.blob(f"{blob_prefix}original.{metadata.get('format','jpg')}')
        img_blob.upload_from_string(metadata["image_bytes"], content_type=metadata.get("content_type","image/jpeg"))
    return {
        "labels_path": labels_blob.name,
        "description_path": desc_blob.name,
        "safety_path": safety_blob.name,
        "original_path": f"{blob_prefix}original.{metadata.get('format','jpg')}" if metadata and metadata.get('format') else None
    }
