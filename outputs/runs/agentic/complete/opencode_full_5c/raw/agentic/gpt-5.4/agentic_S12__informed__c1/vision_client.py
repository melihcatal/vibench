from __future__ import annotations

import base64
import json
import mimetypes
import os
from typing import Any, Dict

import requests
from google.cloud import vision
from openai import OpenAI

from vision_models import ImageSource


GOOGLE_VISION_PROVIDER = "google-cloud-vision"
OPENAI_PROVIDER = "openai"
OPENAI_VISION_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4.1-mini")
OPENAI_TEXT_MODEL = os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini")


def build_image_source(
    image_path: str | None = None,
    image_uri: str | None = None,
    image_bytes: bytes | None = None,
) -> ImageSource:
    if image_bytes is not None:
        return ImageSource(content=image_bytes, mime_type="image/jpeg")
    if image_path:
        mime_type = mimetypes.guess_type(image_path)[0] or "image/jpeg"
        with open(image_path, "rb") as file_obj:
            return ImageSource(content=file_obj.read(), mime_type=mime_type)
    if image_uri:
        return ImageSource(uri=image_uri)
    raise ValueError("One of image_path, image_uri, or image_bytes is required")


def image_source_to_google_image(image: ImageSource) -> vision.Image:
    if image.uri:
        return vision.Image(source=vision.ImageSource(image_uri=image.uri))
    if image.content is None:
        raise ValueError("Image content is required for Google Vision request")
    return vision.Image(content=image.content)


def get_google_vision_client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def image_source_to_openai_input(image: ImageSource) -> Dict[str, Any]:
    if image.uri:
        return {"type": "input_image", "image_url": image.uri}
    if image.content is None:
        raise ValueError("Image content is required for OpenAI vision input")
    encoded = base64.b64encode(image.content).decode("utf-8")
    return {
        "type": "input_image",
        "image_url": f"data:{image.mime_type};base64,{encoded}",
    }


def maybe_json_loads(payload: str) -> Dict[str, Any]:
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        return {"text": payload}


def fetch_binary_image(image_url: str) -> bytes:
    response = requests.get(image_url, timeout=30)
    response.raise_for_status()
    return response.content
