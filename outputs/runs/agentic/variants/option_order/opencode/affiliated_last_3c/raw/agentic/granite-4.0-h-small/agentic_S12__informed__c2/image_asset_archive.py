# image_asset_archive.py
"""Archive image‑analysis artifacts and derived captions in managed object storage.

Supports multiple cloud storage back‑ends; demonstrates Amazon S3 using boto3.
Other providers can be swapped by configuring the appropriate client instance."

import os
import json
import boto3
from botocore.exceptions import NoCredentialsError
from vision_models import archive_artifact

# --- Configuration -----------------------------------------------------------
# Set via environment variables or load from a secrets store
S3_BUCKET = os.getenv("AWS_S3_BUCKET")          # target bucket name
S3_REGION = os.getenv("AWS_S3_REGION", "us-east-1")
S3_KEY = os.getenv("AWS_ACCESS_KEY_ID")
S3_SECRET = os.getenv("AWS_SECRET_ACCESS_KEY")
# ------------------------------------------------------------------------------

def archive_analysis(image_path: str, summary: dict, derived_caption: str) -> None:
    """Persist analysis results and optional caption to object storage.

    The function writes three JSON files:
    * analysis.json – full normalized summary
    * caption.txt   – generated alt‑text (if any)
    * artifact_path – local path of each upload object
    """
    s3 = boto3.client(
        "s3",
        region_name=S3_REGION,
        aws_access_key_id=S3_KEY,
        aws_secret_access_key=S3_SECRET
    )
    # 1. analysis result
    analysis_file = "analysis.json"
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=f"assets/{image_path}/{analysis_file}",
        Body=json.dumps(summary).encode(),
    )
    artifact_path = archive_artifact(analysis_file, S3_BUCKET, s3)
    # 2. caption (if non‑empty)
    if derived_caption.strip():
        caption_file = "caption.txt"
        s3.put_object(
            Bucket=S3_BUCKET,
            Key=f"assets/{image_path}/{caption_file}",
            Body=derived_caption.encode()
        )
        archive_artifact(caption_file, S3_BUCKET, s3)

    print(f"Archived analysis for {image_path} to {S3_BUCKET}/{analysis_file}")
