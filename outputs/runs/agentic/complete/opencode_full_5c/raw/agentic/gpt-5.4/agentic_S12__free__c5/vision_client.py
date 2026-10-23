from __future__ import annotations

import base64
import os
from typing import Any, Dict

import requests
from google.cloud import vision
from openai import OpenAI

from vision_models import ImageInput


GOOGLE_VISION_API_HOST = "vision.googleapis.com"
OPENAI_API_HOST = "api.openai.com"
AWS_S3_HOST = "s3.amazonaws.com"


def get_google_vision_client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


def get_openai_client() -> OpenAI:
    api_key = os.environ["OPENAI_API_KEY"]
    return OpenAI(api_key=api_key)


def build_google_vision_image(image_input: ImageInput) -> vision.Image:
    return vision.Image(content=image_input.image_bytes)


def encode_data_url(image_input: ImageInput) -> str:
    encoded = base64.b64encode(image_input.image_bytes).decode("utf-8")
    return f"data:{image_input.mime_type};base64,{encoded}"


def post_openai_json(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    api_key = os.environ["OPENAI_API_KEY"]
    response = requests.post(
        f"https://{OPENAI_API_HOST}/v1/{path.lstrip('/')}",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def get_s3_bucket_name() -> str:
    return os.environ["S3_ARCHIVE_BUCKET"]
