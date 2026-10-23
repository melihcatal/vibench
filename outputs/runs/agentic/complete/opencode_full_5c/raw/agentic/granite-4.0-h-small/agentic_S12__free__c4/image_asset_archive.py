# image_asset_archive.py
# [LATER-STEP] Archive image-analysis artifacts and derived captions in managed object storage

import os
import json
import uuid
from datetime import datetime
import boto3
from botocore.exceptions import NoCredentialsError

# Provider identification (AWS S3)
PROVIDER = "AWS S3"

# Configure S3 client (expects AWS_ACCESS_KEY_ID & AWS_SECRET_ACCESS_KEY env vars)
S3_CLIENT = boto3.client("s3")
BUCKET_NAME = os.getenv("IMAGE_ARCHIVE_BUCKET", "image-analysis-archive")


def archive_analysis(image_path: str, analysis_results: Dict[str, Any]) -> str:
    """
    Persist original image and its analysis output to S3.

    Args:
        image_path (str): Local path to the source image.
        analysis_results (Dict[str, Any]): Dict produced by earlier steps.

    Returns:
        str: S3 object key of the generated JSON manifest.
    """
    # Generate unique key
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    base_name = os.path.basename(image_path)
    key = f"{timestamp}/{uuid.uuid4().hex}-{base_name}.analysis.json"

    # Store the manifest
    try:
        S3_CLIENT.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=json.dumps(analysis_results).encode("utf-8"),
        )
    except NoCredentialsError:
        raise RuntimeError("AWS credentials not configured for S3 access")

    # Optionally also upload the original image (preserve provenance)
    image_key = f"{timestamp}/{uuid.uuid4().hex}-{base_name}"
    try:
        S3_CLIENT.upload_file(image_path, BUCKET_NAME, image_key)
    except NoCredentialsError:
        raise RuntimeError("AWS credentials not configured for S3 access")

    return key
