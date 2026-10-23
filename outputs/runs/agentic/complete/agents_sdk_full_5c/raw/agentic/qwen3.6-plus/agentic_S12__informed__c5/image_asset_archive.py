"""
Archive image-analysis artifacts and derived captions in managed object storage using Amazon S3.

Provider: Amazon S3
SDK: boto3
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import os
import json
import io
import gzip
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any, Union
from pathlib import Path

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from detect_image_labels import LabelDetectionResponse
from describe_image import ImageDescriptionResponse
from detect_image_text import TextDetectionResponse
from score_image_safety import SafetyModerationResponse


def archive_image_analysis(
    bucket: str,
    object_key: str,
    labels_response: Optional[LabelDetectionResponse] = None,
    description_response: Optional[ImageDescriptionResponse] = None,
    text_response: Optional[TextDetectionResponse] = None,
    safety_response: Optional[SafetyModerationResponse] = None,
    translations: Optional[Dict[str, Dict[str, str]]] = None,
    summary_text: Optional[str] = None,
    source_image_path: Optional[str] = None,
    region: Optional[str] = None,
    compress: bool = True,
    content_type: str = "application/json",
    extra_metadata: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Archive image-analysis artifacts and derived captions into Amazon S3.

    Packages all analysis outputs (labels, descriptions, detected text,
    safety scores, translations, summaries) into a single JSON document
    and uploads it to the specified S3 bucket.

    Args:
        bucket: Target S3 bucket name.
        object_key: S3 object key (path) for the archived artifact.
        labels_response: Output from detect_image_labels.
        description_response: Output from describe_image.
        text_response: Output from detect_image_text.
        safety_response: Output from score_image_safety.
        translations: Output from alt_text_translate.
        summary_text: Summary text from image_summary.
        source_image_path: Original image file path for reference.
        region: AWS region override.
        compress: Whether to gzip the archive before upload.
        content_type: MIME type for the S3 object.
        extra_metadata: Additional S3 user metadata key-value pairs.

    Returns:
        Dict with upload details including S3 URI and ETag.
    """
    s3_client = _create_s3_client(region)

    archive_payload = _build_archive_payload(
        labels_response=labels_response,
        description_response=description_response,
        text_response=text_response,
        safety_response=safety_response,
        translations=translations,
        summary_text=summary_text,
        source_image_path=source_image_path,
    )

    json_bytes = json.dumps(archive_payload, indent=2, default=str).encode("utf-8")

    if compress:
        object_key = object_key + ".gz"
        buf = io.BytesIO()
        with gzip.GzipFile(fileobj=buf, mode="wb") as gz:
            gz.write(json_bytes)
        upload_data = buf.getvalue()
    else:
        upload_data = json_bytes

    upload_kwargs: Dict[str, Any] = {
        "Bucket": bucket,
        "Key": object_key,
        "Body": upload_data,
        "ContentType": "application/gzip" if compress else content_type,
    }

    # Add S3 metadata
    metadata = {
        "archived_at": datetime.now(timezone.utc).isoformat(),
        "source_image": source_image_path or "unknown",
    }
    if extra_metadata:
        metadata.update(extra_metadata)
    upload_kwargs["Metadata"] = metadata

    response = s3_client.put_object(**upload_kwargs)

    etag = response.get("ETag", "").strip('"')

    return {
        "bucket": bucket,
        "key": object_key,
        "s3_uri": f"s3://{bucket}/{object_key}",
        "etag": etag,
        "compressed": compress,
        "content_length": len(upload_data),
        "archived_at": metadata["archived_at"],
    }


def archive_multiple_artifacts(
    bucket: str,
    prefix: str,
    artifacts: List[Dict[str, Any]],
    region: Optional[str] = None,
    compress: bool = True,
) -> List[Dict[str, Any]]:
    """
    Archive multiple image-analysis artifacts under a common S3 prefix.

    Each artifact dict should contain analysis responses and a unique identifier.

    Args:
        bucket: Target S3 bucket name.
        prefix: Common S3 key prefix (e.g., 'analysis/2024-01-15/').
        artifacts: List of artifact dicts with keys like 'id', 'labels_response', etc.
        region: AWS region override.
        compress: Whether to gzip each artifact.

    Returns:
        List of upload result dicts.
    """
    results = []
    for artifact in artifacts:
        artifact_id = artifact.get("id", "unknown")
        object_key = f"{prefix.rstrip('/')}/{artifact_id}/analysis.json"

        result = archive_image_analysis(
            bucket=bucket,
            object_key=object_key,
            labels_response=artifact.get("labels_response"),
            description_response=artifact.get("description_response"),
            text_response=artifact.get("text_response"),
            safety_response=artifact.get("safety_response"),
            translations=artifact.get("translations"),
            summary_text=artifact.get("summary_text"),
            source_image_path=artifact.get("source_image_path"),
            region=region,
            compress=compress,
        )
        results.append(result)

    return results


def archive_captions_only(
    bucket: str,
    image_id: str,
    description_response: ImageDescriptionResponse,
    translations: Optional[Dict[str, Dict[str, str]]] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Archive only image captions and translations (lightweight upload).

    Useful for batch processing where only derived captions need persistence.

    Args:
        bucket: Target S3 bucket name.
        image_id: Unique identifier for the image.
        description_response: Output from describe_image.
        translations: Translated descriptions from alt_text_translate.
        region: AWS region override.

    Returns:
        Upload result dict.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    object_key = f"captions/{image_id}/{timestamp}_captions.json"

    captions_payload = {
        "image_id": image_id,
        "captions": [],
        "translations": translations or {},
        "archived_at": datetime.now(timezone.utc).isoformat(),
    }

    for desc in description_response.descriptions:
        captions_payload["captions"].append({
            "text": desc.text,
            "confidence": desc.confidence,
            "tags": desc.tags,
        })

    s3_client = _create_s3_client(region)
    json_bytes = json.dumps(captions_payload, indent=2, default=str).encode("utf-8")

    response = s3_client.put_object(
        Bucket=bucket,
        Key=object_key,
        Body=json_bytes,
        ContentType="application/json",
        Metadata={
            "image_id": image_id,
            "archived_at": captions_payload["archived_at"],
        },
    )

    etag = response.get("ETag", "").strip('"')

    return {
        "bucket": bucket,
        "key": object_key,
        "s3_uri": f"s3://{bucket}/{object_key}",
        "etag": etag,
    }


def _create_s3_client(region: Optional[str] = None):
    """Create a boto3 S3 client."""
    aws_region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    session_kwargs = {"region_name": aws_region}
    if aws_access_key and aws_secret_key:
        session_kwargs["aws_access_key_id"] = aws_access_key
        session_kwargs["aws_secret_access_key"] = aws_secret_key

    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        s3={"addressing_style": "virtual"},
    )

    return boto3.client("s3", config=config, **session_kwargs)


def _build_archive_payload(
    labels_response: Optional[LabelDetectionResponse] = None,
    description_response: Optional[ImageDescriptionResponse] = None,
    text_response: Optional[TextDetectionResponse] = None,
    safety_response: Optional[SafetyModerationResponse] = None,
    translations: Optional[Dict[str, Dict[str, str]]] = None,
    summary_text: Optional[str] = None,
    source_image_path: Optional[str] = None,
) -> Dict[str, Any]:
    """Build the JSON archive payload from all analysis responses."""
    payload = {
        "metadata": {
            "source_image": source_image_path,
            "archived_at": datetime.now(timezone.utc).isoformat(),
        },
    }

    if labels_response:
        payload["labels"] = {
            "count": len(labels_response.labels),
            "model_version": labels_response.label_model_version,
            "labels": [
                {
                    "name": lbl.name,
                    "confidence": lbl.confidence,
                    "parents": lbl.parents,
                }
                for lbl in labels_response.labels
            ],
        }

    if description_response:
        payload["descriptions"] = {
            "descriptions": [
                {
                    "text": desc.text,
                    "confidence": desc.confidence,
                    "tags": desc.tags,
                }
                for desc in description_response.descriptions
            ],
            "tags": description_response.tags,
        }

    if text_response:
        payload["detected_text"] = {
            "orientation_correction": text_response.orientation_correction,
            "text_regions": [
                {
                    "text": txt.text,
                    "confidence": txt.confidence,
                }
                for txt in text_response.detected_texts
            ],
        }

    if safety_response:
        payload["safety"] = {
            "is_safe": safety_response.is_safe,
            "highest_severity": safety_response.highest_severity,
            "labels": [
                {
                    "category": cat.category,
                    "confidence": cat.confidence,
                    "severity": cat.metadata.get("severity", "unknown"),
                }
                for cat in safety_response.moderation_labels
            ],
        }

    if translations:
        payload["translations"] = translations

    if summary_text:
        payload["summary"] = summary_text

    return payload
