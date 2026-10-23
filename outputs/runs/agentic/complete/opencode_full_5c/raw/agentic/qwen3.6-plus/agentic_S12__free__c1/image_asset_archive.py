from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

from vision_models import (
    DescriptionResponse,
    LabelResponse,
    SafetyResponse,
    TextDetectionResponse,
    description_response_to_dict,
    label_response_to_dict,
    safety_response_to_dict,
    text_detection_response_to_dict,
)

S3_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
S3_ARCHIVE_BUCKET = os.environ.get("VISION_ARCHIVE_BUCKET", "image-analysis-archive")


def get_s3_client(region: Optional[str] = None) -> boto3.client:
    region_name = region or S3_DEFAULT_REGION
    return boto3.client("s3", region_name=region_name)


def build_archive_metadata(
    image_identifier: str,
    labels: Optional[LabelResponse] = None,
    description: Optional[DescriptionResponse] = None,
    text_detection: Optional[TextDetectionResponse] = None,
    safety: Optional[SafetyResponse] = None,
    summary: Optional[str] = None,
    translated_description: Optional[str] = None,
) -> Dict[str, Any]:
    metadata: Dict[str, Any] = {
        "image_identifier": image_identifier,
        "archived_at": datetime.now(timezone.utc).isoformat(),
        "analysis": {
            "labels": label_response_to_dict(labels) if labels else {},
            "description": description_response_to_dict(description)
            if description
            else {},
            "text_detection": text_detection_response_to_dict(text_detection)
            if text_detection
            else {},
            "safety": safety_response_to_dict(safety) if safety else {},
        },
    }
    if summary:
        metadata["summary"] = summary
    if translated_description:
        metadata["translated_description"] = translated_description
    return metadata


def archive_image_artifacts(
    image_identifier: str,
    labels: Optional[LabelResponse] = None,
    description: Optional[DescriptionResponse] = None,
    text_detection: Optional[TextDetectionResponse] = None,
    safety: Optional[SafetyResponse] = None,
    summary: Optional[str] = None,
    translated_description: Optional[str] = None,
    image_data: Optional[bytes] = None,
    bucket: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, str]:
    bucket_name = bucket or S3_ARCHIVE_BUCKET
    s3_client = get_s3_client(region=region)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_id = image_identifier.replace("/", "_").replace("\\", "_").replace(" ", "_")
    prefix = f"analyses/{safe_id}/{timestamp}"

    metadata = build_archive_metadata(
        image_identifier,
        labels,
        description,
        text_detection,
        safety,
        summary,
        translated_description,
    )
    metadata_key = f"{prefix}/analysis_metadata.json"
    s3_client.put_object(
        Bucket=bucket_name,
        Key=metadata_key,
        Body=json.dumps(metadata, indent=2).encode("utf-8"),
        ContentType="application/json",
    )

    uploaded_keys: Dict[str, str] = {"metadata": f"s3://{bucket_name}/{metadata_key}"}

    if image_data:
        image_ext = "jpg"
        image_key = f"{prefix}/source_image.{image_ext}"
        s3_client.put_object(
            Bucket=bucket_name,
            Key=image_key,
            Body=image_data,
            ContentType="image/jpeg",
        )
        uploaded_keys["source_image"] = f"s3://{bucket_name}/{image_key}"

    if description and description.description:
        caption_key = f"{prefix}/caption.txt"
        s3_client.put_object(
            Bucket=bucket_name,
            Key=caption_key,
            Body=description.description.encode("utf-8"),
            ContentType="text/plain",
        )
        uploaded_keys["caption"] = f"s3://{bucket_name}/{caption_key}"

    if translated_description:
        translated_key = f"{prefix}/caption_translated.txt"
        s3_client.put_object(
            Bucket=bucket_name,
            Key=translated_key,
            Body=translated_description.encode("utf-8"),
            ContentType="text/plain",
        )
        uploaded_keys["caption_translated"] = f"s3://{bucket_name}/{translated_key}"

    return uploaded_keys


def archive_batch_artifacts(
    artifacts: List[Dict[str, Any]],
    bucket: Optional[str] = None,
    region: Optional[str] = None,
) -> List[Dict[str, str]]:
    results = []
    for artifact in artifacts:
        result = archive_image_artifacts(
            image_identifier=artifact.get("image_identifier", "unknown"),
            labels=artifact.get("labels"),
            description=artifact.get("description"),
            text_detection=artifact.get("text_detection"),
            safety=artifact.get("safety"),
            summary=artifact.get("summary"),
            translated_description=artifact.get("translated_description"),
            image_data=artifact.get("image_data"),
            bucket=bucket,
            region=region,
        )
        results.append(result)
    return results


if __name__ == "__main__":
    result = archive_image_artifacts(image_identifier="test_image_001.jpg")
    print(result)
