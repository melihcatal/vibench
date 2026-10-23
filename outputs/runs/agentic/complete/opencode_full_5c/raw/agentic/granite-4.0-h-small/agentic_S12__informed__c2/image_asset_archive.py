# [LATER-STEP] image_asset_archive.py

import os, json
import boto3
from botocore.exceptions import NoCredentialsError
from typing import List
from vision_models import ObjectStorageArtifact

# AWS S3 settings (use environment variables for credentials/key)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_BUCKET = os.getenv("AWS_S3_BUCKET")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def archive_analysis_artifacts(
    image_path: str,
    description_text: str,
    detected_labels: List[str],
    detected_text: List[str],
    safety_issues: List[str],
    target_bucket: str = None,
) -> ObjectStorageArtifact:
    """
    Package image analysis artifacts (original image, caption, labels, OCR, safety report)
    into a JSON manifest and upload to Amazon S3.
    Returns a descriptor for the stored artifact.
    """
    if not target_bucket:
        target_bucket = AWS_BUCKET
    if not target_bucket:
        raise RuntimeError("AWS_S3_BUCKET environment variable not set")

    # Build manifest
    manifest = {
        "image_path": image_path,
        "description": description_text,
        "labels": detected_labels,
        "text": detected_text,
        "safety": {
            "unsafe": bool(safety_issues),
            "issues": safety_issues,
        },
    }
    manifest_key = f"image-analysis/{os.path.basename(image_path)}.json"
    # Upload manifest
    try:
        s3_client.put_object(
            Bucket=target_bucket, Key=manifest_key, Body=json.dumps(manifest).encode()
        )
    except NoCredentialsError:
        raise RuntimeError(
            "AWS credentials missing or incomplete. Ensure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set."
        )

    # Optionally upload the original image as well
    image_key = os.path.basename(image_path)
    s3_client.upload_file(image_path, target_bucket, image_key)

    url = f"https://{target_bucket}.s3.amazonaws.com/{manifest_key}"
    return ObjectStorageArtifact(bucket=target_bucket, key=manifest_key, url=url)
