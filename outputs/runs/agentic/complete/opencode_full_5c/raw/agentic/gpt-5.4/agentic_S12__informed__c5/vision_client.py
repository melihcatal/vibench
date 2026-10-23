from __future__ import annotations

import base64
import os

from google.cloud import vision

from vision_models import ImageSource


def get_google_vision_client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


def load_image_source(
    image_path: str | None = None,
    image_uri: str | None = None,
    image_bytes: bytes | None = None,
) -> ImageSource:
    if image_bytes is not None:
        return ImageSource(image_bytes=image_bytes)
    if image_path is not None:
        with open(image_path, "rb") as handle:
            return ImageSource(image_bytes=handle.read())
    if image_uri is not None:
        return ImageSource(image_uri=image_uri)
    raise ValueError("one of image_path, image_uri, or image_bytes is required")


def build_google_vision_image(source: ImageSource) -> vision.Image:
    if source.image_bytes is not None:
        return vision.Image(content=source.image_bytes)
    if source.image_uri is not None:
        return vision.Image(source=vision.ImageSource(image_uri=source.image_uri))
    raise ValueError("image source is empty")


def get_openai_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return api_key


def encode_image_for_openai(source: ImageSource) -> str:
    if source.image_bytes is None:
        raise ValueError("OpenAI vision requests require image bytes")
    return base64.b64encode(source.image_bytes).decode("utf-8")
