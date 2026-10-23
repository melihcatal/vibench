from __future__ import annotations

import base64
import json
import os
from typing import Any, Dict, Iterable

import boto3
from google.cloud import vision
from openai import OpenAI

from vision_models import ImageInput


def load_image_input(image_path: str, mime_type: str = "image/jpeg") -> ImageInput:
    with open(image_path, "rb") as handle:
        return ImageInput(
            image_bytes=handle.read(), mime_type=mime_type, source_uri=image_path
        )


def to_google_vision_image(image: ImageInput) -> vision.Image:
    return vision.Image(content=image.image_bytes)


def build_data_url(image: ImageInput) -> str:
    encoded = base64.b64encode(image.image_bytes).decode("utf-8")
    return f"data:{image.mime_type};base64,{encoded}"


def get_google_vision_client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.environ.get("AWS_SESSION_TOKEN"),
        region_name=os.environ.get("AWS_REGION")
        or os.environ.get("AWS_DEFAULT_REGION")
        or "us-east-1",
    )


def get_archive_bucket() -> str:
    bucket = os.environ.get("S3_ARCHIVE_BUCKET")
    if not bucket:
        raise ValueError("S3_ARCHIVE_BUCKET is required")
    return bucket


def json_bytes(payload: Dict[str, Any]) -> bytes:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")


def combine_lines(values: Iterable[str]) -> str:
    return "\n".join(value for value in values if value)
