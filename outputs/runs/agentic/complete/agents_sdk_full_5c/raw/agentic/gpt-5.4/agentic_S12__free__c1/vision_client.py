from __future__ import annotations

import base64
import os
from typing import Optional

from google.cloud import vision

from vision_models import ImageSource


GOOGLE_VISION_PROVIDER = "google-cloud-vision"
GOOGLE_VISION_MODEL = "builtin/latest"


def get_google_vision_client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


def build_google_image(image: ImageSource) -> vision.Image:
    if image.image_uri:
        return vision.Image(source=vision.ImageSource(image_uri=image.image_uri))
    if image.image_bytes:
        return vision.Image(content=image.image_bytes)
    raise ValueError("ImageSource requires image_bytes or image_uri")


def load_image_source(*, image_path: Optional[str] = None, image_uri: Optional[str] = None, mime_type: str = "image/jpeg") -> ImageSource:
    if image_uri:
        return ImageSource(image_uri=image_uri, mime_type=mime_type)
    if image_path:
        with open(image_path, "rb") as handle:
            return ImageSource(image_bytes=handle.read(), mime_type=mime_type)
    raise ValueError("Either image_path or image_uri must be provided")


def encode_image_base64(image: ImageSource) -> str:
    if not image.image_bytes:
        raise ValueError("Base64 encoding requires local image bytes")
    return base64.b64encode(image.image_bytes).decode("utf-8")


def google_credentials_path() -> Optional[str]:
    return os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
