import base64
import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI

OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


def build_openai_client() -> OpenAI:
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return OpenAI(api_key=api_key)


def image_input_from_path_or_bytes(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None) -> str:
    if image_path:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
    if not image_bytes:
        raise ValueError("image_path or image_bytes is required")
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:image/png;base64,{encoded}"
