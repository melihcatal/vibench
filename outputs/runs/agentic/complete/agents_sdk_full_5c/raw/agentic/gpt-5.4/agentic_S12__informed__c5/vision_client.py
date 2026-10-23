from __future__ import annotations

import base64
import os
from typing import Optional

from google.cloud import vision


DEFAULT_PROVIDER = "google-cloud-vision"


def get_vision_client() -> vision.ImageAnnotatorClient:
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS is required for Google Cloud Vision")
    return vision.ImageAnnotatorClient()


def load_image_bytes(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None) -> bytes:
    if image_bytes is not None:
        return image_bytes
    if not image_path:
        raise ValueError("Provide image_path or image_bytes")
    with open(image_path, "rb") as infile:
        return infile.read()


def make_vision_image(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None) -> vision.Image:
    content = load_image_bytes(image_path=image_path, image_bytes=image_bytes)
    return vision.Image(content=content)


def image_bytes_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")
