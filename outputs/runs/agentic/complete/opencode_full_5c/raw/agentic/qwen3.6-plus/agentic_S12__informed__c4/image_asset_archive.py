import os
import json
import datetime
from typing import List, Optional

import boto3
from botocore.config import Config

from vision_models import (
    ArchiveRequest,
    ArchiveResponse,
    LabelDetectionResponse,
    ImageDescriptionResponse,
    TextDetectionResponse,
    SafetyScoreResponse,
    ImageSummaryResponse,
    TranslationResponse,
    TextSafetyResponse,
)


AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
DEFAULT_BUCKET = os.environ.get("IMAGE_ARCHIVE_BUCKET", "image-analysis-archive")


def get_s3_client() -> boto3.client:
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION,
    )
    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
    )
    return session.client("s3", config=config)


def archive_image_artifacts(request: ArchiveRequest) -> ArchiveResponse:
    client = get_s3_client()
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    prefix = request.prefix.rstrip("/") if request.prefix else "image-analysis"

    archived_keys = []

    for artifact_name, artifact_data in request.artifacts.items():
        key = f"{prefix}/{timestamp}/{artifact_name}"

        if isinstance(artifact_data, (dict, list)):
            body = json.dumps(artifact_data, default=str, indent=2).encode("utf-8")
            content_type = "application/json"
        elif isinstance(artifact_data, bytes):
            body = artifact_data
            content_type = "application/octet-stream"
        else:
            body = str(artifact_data).encode("utf-8")
            content_type = "text/plain"

        client.put_object(
            Bucket=request.bucket_name,
            Key=key,
            Body=body,
            ContentType=content_type,
        )
        archived_keys.append(key)

    return ArchiveResponse(
        archived_keys=archived_keys,
        bucket=request.bucket_name,
        model="amazon-s3",
    )


def archive_analysis_results(
    labels_response: Optional[LabelDetectionResponse] = None,
    description_response: Optional[ImageDescriptionResponse] = None,
    text_response: Optional[TextDetectionResponse] = None,
    safety_response: Optional[SafetyScoreResponse] = None,
    summary_response: Optional[ImageSummaryResponse] = None,
    translation_response: Optional[TranslationResponse] = None,
    text_safety_response: Optional[TextSafetyResponse] = None,
    bucket_name: str = DEFAULT_BUCKET,
    prefix: str = "image-analysis",
) -> ArchiveResponse:
    artifacts = {}

    if labels_response:
        artifacts["labels.json"] = {
            "labels": [
                {"name": l.name, "confidence": l.confidence, "parents": l.parent_labels}
                for l in labels_response.labels
            ],
            "image_width": labels_response.image_width,
            "image_height": labels_response.image_height,
            "model": labels_response.model,
        }

    if description_response:
        artifacts["description.json"] = {
            "description": description_response.description,
            "tags": description_response.tags,
            "confidence": description_response.confidence,
            "model": description_response.model,
        }

    if text_response:
        artifacts["text_detection.json"] = {
            "detected_texts": [
                {"text": t.text, "confidence": t.confidence}
                for t in text_response.detected_texts
            ],
            "full_text": text_response.full_text,
            "model": text_response.model,
        }

    if safety_response:
        artifacts["safety.json"] = {
            "is_safe": safety_response.is_safe,
            "categories": [
                {"name": c.name, "confidence": c.confidence}
                for c in safety_response.categories
            ],
            "threshold": safety_response.threshold,
            "model": safety_response.model,
        }

    if summary_response:
        artifacts["summary.json"] = {
            "summary": summary_response.summary,
            "model": summary_response.model,
        }

    if translation_response:
        artifacts["translation.json"] = {
            "translated_text": translation_response.translated_text,
            "source_language": translation_response.source_language,
            "target_language": translation_response.target_language,
            "model": translation_response.model,
        }

    if text_safety_response:
        artifacts["text_safety.json"] = {
            "is_safe": text_safety_response.is_safe,
            "scores": [
                {"category": s.category, "score": s.score}
                for s in text_safety_response.scores
            ],
            "model": text_safety_response.model,
        }

    archive_request = ArchiveRequest(
        bucket_name=bucket_name,
        prefix=prefix,
        artifacts=artifacts,
    )

    return archive_image_artifacts(archive_request)
