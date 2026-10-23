"""
image_asset_archive.py - Archive image-analysis artifacts and derived captions
in managed object storage using Amazon S3.

Provider: Amazon S3 (boto3 SDK)
API hostname: https://s3.{region}.amazonaws.com
"""

import os
import json
import io
import zipfile
from datetime import datetime
from typing import List, Dict, Any, Optional

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from vision_client import load_image_as_bytes
from detect_image_labels import detect_labels_from_bytes
from describe_image import describe_image_from_bytes
from detect_image_text import detect_text_from_bytes
from score_image_safety import score_image_safety_from_bytes
from vision_models import (
    LabelDetectionResponse,
    ImageDescriptionResponse,
    TextDetectionResponse,
    ImageSafetyResponse,
)

AWS_S3_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_S3_BUCKET = os.environ.get("VISION_ARCHIVE_S3_BUCKET", "vision-analysis-archive")


def get_s3_client() -> boto3.client:
    """Create and return a configured Amazon S3 client."""
    session = boto3.Session(
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=AWS_S3_REGION,
    )
    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        connect_timeout=10,
        read_timeout=60,
    )
    return session.client("s3", config=config)


def build_analysis_artifact(
    labels_response: LabelDetectionResponse,
    description_response: ImageDescriptionResponse,
    text_response: TextDetectionResponse,
    safety_response: ImageSafetyResponse,
    image_path: str,
) -> Dict[str, Any]:
    """Build a structured artifact dictionary from all analysis results."""
    return {
        "source_image": image_path,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "analysis": {
            "labels": {
                "count": len(labels_response.labels),
                "labels": [
                    {
                        "name": l.name,
                        "confidence": l.confidence,
                        "parents": l.parents,
                    }
                    for l in labels_response.labels
                ],
            },
            "description": {
                "text": description_response.description,
                "labels_used": description_response.labels_used,
            },
            "text_detection": {
                "count": len(text_response.detected_text),
                "texts": [
                    {
                        "text": t.text,
                        "confidence": t.confidence,
                    }
                    for t in text_response.detected_text
                ],
            },
            "safety": {
                "is_safe": safety_response.is_safe,
                "findings": [
                    {
                        "category": f.category,
                        "confidence": f.confidence,
                    }
                    for f in safety_response.findings
                ],
            },
        },
    }


def archive_to_s3(
    artifact: Dict[str, Any],
    image_bytes: bytes,
    s3_bucket: Optional[str] = None,
    s3_key_prefix: Optional[str] = None,
) -> Dict[str, str]:
    """
    Archive image-analysis artifacts and derived captions to Amazon S3.

    Creates a ZIP archive containing the original image, analysis JSON metadata,
    and a plain-text caption file, then uploads it to the specified S3 bucket.

    Args:
        artifact: Structured analysis artifact dictionary.
        image_bytes: Raw bytes of the original image.
        s3_bucket: S3 bucket name. Defaults to env VISION_ARCHIVE_S3_BUCKET.
        s3_key_prefix: Optional S3 key prefix for organizing uploads.

    Returns:
        Dictionary with S3 upload details (bucket, key, version_id).
    """
    bucket = s3_bucket or AWS_S3_BUCKET
    client = get_s3_client()

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    source_image = artifact.get("source_image", "unknown")
    base_name = os.path.splitext(os.path.basename(source_image))[0]

    if s3_key_prefix:
        archive_key = f"{s3_key_prefix}/{base_name}_{timestamp}.zip"
    else:
        archive_key = f"vision-archives/{base_name}_{timestamp}.zip"

    # Build ZIP archive in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        # Original image
        image_ext = os.path.splitext(source_image)[1] or ".jpg"
        zf.writestr(f"{base_name}_original{image_ext}", image_bytes)

        # Analysis metadata JSON
        metadata_json = json.dumps(artifact, indent=2, default=str)
        zf.writestr(f"{base_name}_analysis.json", metadata_json)

        # Plain text caption
        caption = artifact.get("analysis", {}).get("description", {}).get("text", "")
        zf.writestr(f"{base_name}_caption.txt", caption)

        # Labels list
        labels = artifact.get("analysis", {}).get("labels", {}).get("labels", [])
        labels_text = "\n".join(
            f"{l['name']} ({l['confidence']:.1f}%)" for l in labels
        )
        zf.writestr(f"{base_name}_labels.txt", labels_text)

    zip_buffer.seek(0)

    # Upload to S3
    upload_response = client.put_object(
        Bucket=bucket,
        Key=archive_key,
        Body=zip_buffer.getvalue(),
        ContentType="application/zip",
        Metadata={
            "source-image": base_name,
            "analysis-timestamp": artifact.get("timestamp", ""),
            "is-safe": str(artifact.get("analysis", {}).get("safety", {}).get("is_safe", "")),
        },
    )

    return {
        "bucket": bucket,
        "key": archive_key,
        "version_id": upload_response.get("VersionId"),
        "etag": upload_response.get("ETag", "").strip('"'),
    }


def archive_analysis_result(
    image_path: str,
    s3_bucket: Optional[str] = None,
    s3_key_prefix: Optional[str] = None,
    min_confidence: float = 50.0,
) -> Dict[str, str]:
    """
    Run full image analysis and archive all artifacts to Amazon S3.

    Performs label detection, image description, text detection, and safety
    scoring, then bundles everything into a ZIP archive stored in S3.

    Args:
        image_path: Path to the local image file.
        s3_bucket: Target S3 bucket name.
        s3_key_prefix: Optional S3 key prefix.
        min_confidence: Confidence threshold for analyses.

    Returns:
        Dictionary with S3 upload details.
    """
    image_bytes = load_image_as_bytes(image_path)

    labels_response = detect_labels_from_bytes(image_bytes, min_confidence=min_confidence)
    description_response = describe_image_from_bytes(image_bytes, min_confidence=min_confidence)
    text_response = detect_text_from_bytes(image_bytes, min_confidence=min_confidence)
    safety_response = score_image_safety_from_bytes(image_bytes, min_confidence=min_confidence)

    artifact = build_analysis_artifact(
        labels_response, description_response, text_response, safety_response, image_path
    )

    return archive_to_s3(artifact, image_bytes, s3_bucket, s3_key_prefix)


def download_archive_from_s3(
    s3_bucket: str,
    s3_key: str,
    local_path: str,
) -> str:
    """
    Download a previously archived image-analysis ZIP from Amazon S3.

    Args:
        s3_bucket: S3 bucket name.
        s3_key: S3 object key.
        local_path: Local file path to save the downloaded archive.

    Returns:
        Path to the downloaded local file.
    """
    client = get_s3_client()
    client.download_file(s3_bucket, s3_key, local_path)
    return local_path


def list_archives_in_s3(
    s3_bucket: Optional[str] = None,
    prefix: str = "vision-archives/",
) -> List[Dict[str, Any]]:
    """
    List archived image-analysis artifacts in Amazon S3.

    Args:
        s3_bucket: S3 bucket name.
        prefix: S3 key prefix to filter objects.

    Returns:
        List of archive metadata dictionaries.
    """
    bucket = s3_bucket or AWS_S3_BUCKET
    client = get_s3_client()

    response = client.list_objects_v2(
        Bucket=bucket,
        Prefix=prefix,
    )

    archives = []
    for obj in response.get("Contents", []):
        archives.append({
            "key": obj["Key"],
            "size_bytes": obj["Size"],
            "last_modified": obj["LastModified"].isoformat(),
            "etag": obj["ETag"].strip('"'),
        })

    return archives
