from __future__ import annotations

import base64
import os
from pathlib import Path
from typing import Optional

from google.cloud import vision


GOOGLE_VISION_ENDPOINT = os.getenv("GOOGLE_CLOUD_VISION_ENDPOINT", "vision.googleapis.com")
GOOGLE_VISION_MODEL = "builtin/latest"


def get_vision_client(credentials_path: Optional[str] = None) -> vision.ImageAnnotatorClient:
    if credentials_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    return vision.ImageAnnotatorClient(client_options={"api_endpoint": GOOGLE_VISION_ENDPOINT})


def load_image_bytes(image_path: str) -> bytes:
    return Path(image_path).read_bytes()


def load_image_uri(image_uri: str) -> vision.Image:
    return vision.Image(source=vision.ImageSource(image_uri=image_uri))


def load_image_content(image_path: str) -> vision.Image:
    return vision.Image(content=load_image_bytes(image_path))


def image_to_data_url(image_path: str, mime_type: str = "image/jpeg") -> str:
    payload = base64.b64encode(load_image_bytes(image_path)).decode("utf-8")
    return f"data:{mime_type};base64,{payload}"
