# image_asset_archive.py
# [LATER-STEP]

import os
import json
import shutil
from pathlib import Path


# Placeholder for cloud storage SDK (e.g., AWS S3, GCS)
class CloudStorage:
    """Stub for cloud storage client.
    Replace with real SDK calls (e.g., boto3, google-cloud-storage)."
    """

    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        # Example: boto3.client('s3') or google.cloud.storage.Client()

    def upload_json(self, key: str, data: dict):
        """Store a JSON payload as an object."""
        # Placeholder: in real implementation, serialize and upload to bucket/key
        print(f"[STUB] Uploading JSON to {self.bucket_name}/{key}")

    def upload_file(self, src_path: str, dest_key: str):
        """Copy a local file to the bucket."""
        # Placeholder: real upload logic here
        print(f"[STUB] Uploading file {src_path} to {self.bucket_name}/{dest_key}")


# Configuration (replace with environment variables or config file)
DEFAULT_BUCKET = os.getenv("ARCHIVE_BUCKET", "image-analysis-archive")

# Singleton client instance (simple example)
archive_client = CloudStorage(DEFAULT_BUCKET)


def archive_analysis(image_path: str, labels: list, caption: str, safety: dict):
    """Archive the raw image, extracted labels, caption, and safety report.
    All artifacts are stored as separate objects under a common prefix."""
    # Determine a deterministic archive prefix (e.g., based on image name)
    base_name = Path(image_path).stem
    prefix = f"analysis/{base_name}/"

    # Store raw image (if accessible; here we just note the path)
    archive_client.upload_file(image_path, prefix + "original_image.jpg")

    # Store labels
    labels_key = prefix + "labels.json"
    archive_client.upload_json(labels_key, {"labels": labels})

    # Store caption
    caption_key = prefix + "caption.txt"
    archive_client.upload_file(caption, caption_key)

    # Store safety report
    safety_key = prefix + "safety.json"
    archive_client.upload_json(safety_key, {"safety": safety})

    print(f'[INFO] Analysis assets for "{image_path}" archived under prefix {prefix}')


# Example usage (would be called from later-step orchestration)
if __name__ == "__main__":
    dummy_path = "sample.jpg"
    dummy_labels = [{"name": "cat", "confidence": 0.98}]
    dummy_caption = "A domestic cat sitting on a windowsill."
    dummy_safety = {"adult": "UNLIKELY", "violence": "UNLIKELY"}
    archive_analysis(dummy_path, dummy_labels, dummy_caption, dummy_safety)
