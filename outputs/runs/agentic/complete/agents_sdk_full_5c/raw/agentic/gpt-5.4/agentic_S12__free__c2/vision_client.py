from __future__ import annotations

import base64
import mimetypes
import os
from typing import Optional

from google.cloud import vision
from openai import OpenAI

from vision_models import ImageSource


GOOGLE_APPLICATION_CREDENTIALS_ENV = "GOOGLE_APPLICATION_CREDENTIALS"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
GCS_BUCKET_ENV = "GCS_BUCKET_NAME"


def load_image_source(image_path: str) -> ImageSource:
    mime_type, _ = mimetypes.guess_type(image_path)
    with open(image_path, "rb") as handle:
        content = handle.read()
    return ImageSource(image_path=image_path, image_bytes=content, mime_type=mime_type or "image/jpeg")


def image_bytes_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("ascii")


def build_google_vision_client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


def build_openai_client(api_key: Optional[str] = None) -> OpenAI:
    return OpenAI(api_key=api_key or os.environ.get(OPENAI_API_KEY_ENV))


def ensure_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value
