# image_asset_archive.py
import os
import json
import boto3
from botocore.exceptions import ClientError


def archive_assets(image_path, summary_data):
    """Archive image and its analysis artifacts to Amazon S3."""
    s3 = boto3.client("s3")
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    bucket = os.getenv("ARCHIVE_BUCKET")
    if not bucket:
        raise RuntimeError("ARCHIVE_BUCKET environment variable not set")
    try:
        # Upload original image
        s3.upload_file(image_path, bucket, f"{base_name}.png")
        # Upload summary JSON
        s3.upload_file(summary_data["output_path"], bucket, f"{base_name}_summary.json")
        # Optionally upload OCR text files or other artifacts here
    except ClientError as e:
        raise RuntimeError(f"Failed to upload assets: {e}")

    return {
        "bucket": bucket,
        "image_key": f"{base_name}.png",
        "summary_key": f"{base_name}_summary.json",
    }
