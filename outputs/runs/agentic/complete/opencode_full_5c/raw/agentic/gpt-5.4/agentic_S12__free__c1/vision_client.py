from __future__ import annotations

import base64
import os
from typing import Any

import boto3
from google.cloud import vision_v1
from openai import OpenAI

from vision_models import ImageInput


GOOGLE_VISION_ENDPOINT = "vision.googleapis.com"
OPENAI_MODEL = "gpt-4.1-mini"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"
AWS_S3_SERVICE = "s3"


def load_image_input(
    image_path: str | None = None,
    image_uri: str | None = None,
    mime_type: str = "image/jpeg",
) -> ImageInput:
    if image_path:
        with open(image_path, "rb") as handle:
            return ImageInput(image_bytes=handle.read(), mime_type=mime_type)
    if image_uri:
        return ImageInput(image_uri=image_uri, mime_type=mime_type)
    raise ValueError("Either image_path or image_uri is required")


def image_to_data_url(image: ImageInput) -> str:
    if not image.image_bytes:
        raise ValueError("image_bytes are required for OpenAI vision requests")
    encoded = base64.b64encode(image.image_bytes).decode("utf-8")
    return f"data:{image.mime_type};base64,{encoded}"


def get_google_vision_client() -> vision_v1.ImageAnnotatorClient:
    return vision_v1.ImageAnnotatorClient()


def build_google_vision_image(image: ImageInput) -> vision_v1.Image:
    if image.image_bytes:
        return vision_v1.Image(content=image.image_bytes)
    if image.image_uri:
        return vision_v1.Image(source=vision_v1.ImageSource(image_uri=image.image_uri))
    raise ValueError("Image input is empty")


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def get_s3_client() -> Any:
    region_name = (
        os.environ.get("AWS_REGION")
        or os.environ.get("AWS_DEFAULT_REGION")
        or "us-east-1"
    )
    return boto3.client(AWS_S3_SERVICE, region_name=region_name)
