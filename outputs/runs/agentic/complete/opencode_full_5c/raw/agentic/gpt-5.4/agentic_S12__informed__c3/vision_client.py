from __future__ import annotations

import base64
import mimetypes
import os
from typing import Optional

from google.cloud import vision
from openai import OpenAI


GOOGLE_VISION_PROVIDER = "google-cloud-vision"
OPENAI_PROVIDER = "openai"
OPENAI_VISION_MODEL = "gpt-4.1-mini"


def get_google_vision_client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


def get_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    return OpenAI(api_key=api_key)


def load_image_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as infile:
        return infile.read()


def build_google_vision_image(
    image_path: Optional[str] = None, image_uri: Optional[str] = None
) -> vision.Image:
    if image_path:
        return vision.Image(content=load_image_bytes(image_path))
    if image_uri:
        return vision.Image(source=vision.ImageSource(image_uri=image_uri))
    raise ValueError("Either image_path or image_uri is required")


def build_openai_image_input(
    image_path: Optional[str] = None, image_uri: Optional[str] = None
) -> dict:
    if image_uri:
        return {"type": "input_image", "image_url": image_uri}
    if image_path:
        image_bytes = load_image_bytes(image_path)
        media_type = mimetypes.guess_type(image_path)[0] or "image/jpeg"
        encoded = base64.b64encode(image_bytes).decode("utf-8")
        return {
            "type": "input_image",
            "image_url": f"data:{media_type};base64,{encoded}",
        }
    raise ValueError("Either image_path or image_uri is required")
