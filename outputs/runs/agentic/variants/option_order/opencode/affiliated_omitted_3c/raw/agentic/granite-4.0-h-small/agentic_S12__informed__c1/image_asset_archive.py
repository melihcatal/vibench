# image_asset_archive.py - Archive image-analysis artifacts and derived captions in managed object storage (Amazon S3)

import os
import json
import boto3
from typing import List, Dict, Any

# AWS credentials (use env vars AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in production)
S3_BUCKET = os.getenv("S3_BUCKET", "your-archive-bucket")
S3_PREFIX = os.getenv("S3_PREFIX", "image-analysis/")

S3_CLIENT = boto3.client(
    "s3",
    region_name="us-east-1",
    # credentials are auto-loaded from env vars
)


def archive_analysis(analysis_results: Dict[str, Any], image_id: str):
    """
    Store a JSON snapshot of all same-scenario results and optionally the original image.

    Parameters:
      analysis_results: dict containing keys 'labels', 'description', 'text', 'safety'
      image_id: unique identifier for the original image (e.g., filename or UUID)
    """
    # Serialize results to JSON
    archive_data = {
        "image_id": image_id,
        "analysis": analysis_results,
        "generated_at": os.getenv("GENERATED_AT", str(int(os.time()))),
    }
    json_body = json.dumps(archive_data, ensure_ascii=False, indent=2)
    key = f"{S3_PREFIX}{image_id}.json"
    try:
        S3_CLIENT.put_object(Bucket=S3_BUCKET, Key=key, Body=json_body.encode("utf-8"))
        print(f"[INFO] Archived analysis for {image_id} to s3://{S3_BUCKET}/{key}")
    except Exception as e:
        print(f"[ERROR] Failed to archive: {e}")


def upload_original_image(image_path: str, image_id: str):
    """Upload the original image file to the same bucket (optional)."""
    try:
        S3_CLIENT.upload_file(image_path, S3_BUCKET, f"{S3_PREFIX}{image_id}.original")
        print(
            f"[INFO] Uploaded original image for {image_id} to s3://{S3_BUCKET}/{S3_PREFIX}{image_id}.original"
        )
    except Exception as e:
        print(f"[ERROR] Failed to upload original image: {e}")


if __name__ == "__main__":
    # Simple CLI for testing; assumes analysis_results is provided as a JSON file
    import sys, json

    if len(sys.argv) < 3:
        print(
            "Usage: image_asset_archive.py <analysis_json_file> <image_id> [<original_image_path>]"
        )
        sys.exit(1)
    analysis_json = sys.argv[1]
    img_id = sys.argv[2]
    original_path = sys.argv[3] if len(sys.argv) > 3 else None
    with open(analysis_json, "r", encoding="utf-8") as f:
        analysis = json.load(f)
    archive_analysis(analysis, img_id)
    if original_path:
        upload_original_image(original_path, img_id)
