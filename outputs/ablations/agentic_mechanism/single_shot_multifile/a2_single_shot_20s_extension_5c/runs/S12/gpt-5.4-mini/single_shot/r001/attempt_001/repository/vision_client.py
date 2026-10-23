import base64
import mimetypes
import os
from pathlib import Path
from typing import Optional

AZURE_VISION_ENDPOINT_ENV = "AZURE_VISION_ENDPOINT"
AZURE_VISION_KEY_ENV = "AZURE_VISION_API_KEY"


def get_vision_endpoint() -> str:
    endpoint = os.environ.get(AZURE_VISION_ENDPOINT_ENV, "").strip()
    if not endpoint:
        raise ValueError("AZURE_VISION_ENDPOINT is required")
    return endpoint


def get_vision_api_key() -> str:
    api_key = os.environ.get(AZURE_VISION_KEY_ENV, "").strip()
    if not api_key:
        raise ValueError("AZURE_VISION_API_KEY is required")
    return api_key


def image_to_data_url(image_path: str) -> str:
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(image_path)
    mime, _ = mimetypes.guess_type(str(path))
    if not mime:
        mime = "image/jpeg"
    data = path.read_bytes()
    encoded = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{encoded}"
