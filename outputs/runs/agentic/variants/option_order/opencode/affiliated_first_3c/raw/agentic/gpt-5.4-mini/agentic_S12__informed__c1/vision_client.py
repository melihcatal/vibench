import base64
import os
from typing import Any, Dict, Optional

import requests

from vision_models import VisionImageInput


AZURE_VISION_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT", "")
AZURE_VISION_KEY = os.getenv("AZURE_VISION_KEY", "")


def load_image_bytes(image: VisionImageInput) -> bytes:
    if image.bytes_data is not None:
        return image.bytes_data
    if image.path:
        with open(image.path, "rb") as f:
            return f.read()
    if image.url:
        response = requests.get(image.url, timeout=30)
        response.raise_for_status()
        return response.content
    raise ValueError("image input requires path, url, or bytes_data")


def encode_image_base64(image: VisionImageInput) -> str:
    return base64.b64encode(load_image_bytes(image)).decode("ascii")


def azure_vision_headers() -> Dict[str, str]:
    if not AZURE_VISION_KEY:
        raise ValueError("AZURE_VISION_KEY is required")
    return {
        "Ocp-Apim-Subscription-Key": AZURE_VISION_KEY,
        "Content-Type": "application/json",
    }


def azure_vision_endpoint(path: str) -> str:
    if not AZURE_VISION_ENDPOINT:
        raise ValueError("AZURE_VISION_ENDPOINT is required")
    return AZURE_VISION_ENDPOINT.rstrip("/") + path


def post_json(url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post(
        url, headers=azure_vision_headers(), json=payload, timeout=60
    )
    response.raise_for_status()
    return response.json()
