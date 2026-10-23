# image_asset_archive.py
"""Later-step integration: Archive image‑analysis artifacts and derived captions.

Stores assets in Google Cloud Storage (GCS) using the google-cloud-storage SDK (identifiable in code).
"""

from google.cloud import storage
import os
import uuid
from datetime import datetime

# Provider identifiers (Google Cloud Storage)
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


def archive_assets(
    image_path: str,
    caption: str,
    labels: list[dict],
    ocr: list[str],
    safety_score: float,
):
    """Package analysis results and upload them to a managed GCS bucket.

    Args:
        image_path: Local path of the original image file.
        caption: The generated visual description.
        labels: List of normalized labels from detection.
        ocr: List of extracted text strings.
        safety_score: Numeric risk score from safety evaluation.
    """
    # Initialize GCS client with credentials file
    client = storage.Client.from_service_account_json(GOOGLE_APPLICATION_CREDENTIALS)
    # Choose (or create) bucket name – a fixed name for demo purposes
    bucket_name = "vibench-image-assets"
    bucket = client.bucket(bucket_name)
    # Optional: create bucket if it does not exist (requires OWNER permissions)
    try:
        client.create_bucket(bucket_name)
    except Exception:
        pass  # bucket already exists, continue
    # Generate a unique filename based on timestamp and image hash
    image_hash = uuid.uuid4().hex[:8]
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    filename = (
        f"{os.path.basename(image_path).replace('.', '')}_{timestamp}_{image_hash}.json"
    )
    blob = bucket.blob(filename)
    # Build a JSON payload containing all artifacts
    payload = {
        "caption": caption,
        "labels": labels,
        "ocr": ocr,
        "safety_score": safety_score,
        "metadata": {
            "original_filename": os.path.basename(image_path),
            "uploaded_at_utc": timestamp,
        },
    }
    # Upload JSON file
    blob.upload_from_string(json.dumps(payload, indent=2))
    print(f"Archived assets to GCS: gs://{bucket_name}/{filename}")
