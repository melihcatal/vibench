from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Optional

import boto3

try:
    from google.cloud import vision
except Exception:
    vision = None

from storage_client import get_bucket_name, get_storage_config
from storage_models import StorageObjectRequest, normalize_object_metadata


@dataclass(slots=True)
class OCRResult:
    bucket: str
    key: str
    text: str
    language: str | None = None
    metadata: dict[str, Any] | None = None


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value not in (None, "") else default


def _get_object_bytes(bucket: str, key: str) -> tuple[bytes, dict[str, Any]]:
    config = get_storage_config()
    client = boto3.client(
        "s3",
        region_name=config.region_name,
        endpoint_url=config.endpoint_url,
        use_ssl=config.use_ssl,
        aws_access_key_id=config.access_key_id,
        aws_secret_access_key=config.secret_access_key,
        aws_session_token=config.session_token,
    )
    response = client.get_object(Bucket=bucket, Key=key)
    body = response["Body"].read()
    metadata = {
        "content_type": response.get("ContentType"),
        "content_length": response.get("ContentLength"),
        "etag": response.get("ETag"),
        "last_modified": response.get("LastModified"),
        "metadata": response.get("Metadata", {}),
    }
    return body, metadata


def _vision_client():
    if vision is None:
        raise RuntimeError("google-cloud-vision is required for OCR")
    return vision.ImageAnnotatorClient()


def run_stored_document_ocr(bucket: str | None, key: str) -> OCRResult:
    request = StorageObjectRequest(bucket=bucket or get_bucket_name(), key=key)
    document_bytes, metadata = _get_object_bytes(request.bucket, request.key)
    client = _vision_client()
    image = vision.Image(content=document_bytes)
    response = client.document_text_detection(image=image)
    if response.error.message:
        raise RuntimeError(response.error.message)
    text = response.full_text_annotation.text if response.full_text_annotation else ""
    language = None
    if response.full_text_annotation and response.full_text_annotation.pages:
        symbols = response.full_text_annotation.pages[0].property.detected_languages
        if symbols:
            language = symbols[0].language_code
    return OCRResult(
        bucket=request.bucket,
        key=request.key,
        text=text,
        language=language,
        metadata=normalize_object_metadata(metadata),
    )


def stored_document_ocr(bucket: str | None, key: str) -> dict[str, Any]:
    result = run_stored_document_ocr(bucket, key)
    return {
        "bucket": result.bucket,
        "key": result.key,
        "text": result.text,
        "language": result.language,
        "metadata": result.metadata or {},
    }
