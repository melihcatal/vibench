import base64
import os
from pathlib import Path
from typing import Optional

from openai import OpenAI


def build_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return OpenAI(api_key=api_key)


def image_to_data_url(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None, image_url: Optional[str] = None) -> str:
    if image_url:
        return image_url
    if image_bytes is None and image_path is None:
        raise ValueError("One of image_path, image_bytes, or image_url must be provided")
    if image_bytes is None and image_path is not None:
        image_bytes = Path(image_path).read_bytes()
    if image_bytes is None:
        raise ValueError("Unable to read image bytes")
    encoded = base64.b64encode(image_bytes).decode("ascii")
    return f"data:image/png;base64,{encoded}"
