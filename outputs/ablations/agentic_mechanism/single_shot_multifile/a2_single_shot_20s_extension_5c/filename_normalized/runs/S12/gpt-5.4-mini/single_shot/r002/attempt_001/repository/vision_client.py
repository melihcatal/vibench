import base64
import mimetypes
import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class VisionConfig:
    openai_api_key: str
    openai_base_url: str
    vision_model: str
    mime_type: str


def load_vision_config() -> VisionConfig:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return VisionConfig(
        openai_api_key=api_key,
        openai_base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        vision_model=os.environ.get("OPENAI_VISION_MODEL", "gpt-4o-mini"),
        mime_type=os.environ.get("VISION_IMAGE_MIME_TYPE", "image/jpeg"),
    )


def read_image_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()


def to_data_url(image_bytes: bytes, mime_type: str = "image/jpeg") -> str:
    return f"data:{mime_type};base64,{base64.b64encode(image_bytes).decode('ascii')}"


def guess_mime_type(image_path: str) -> str:
    guessed, _ = mimetypes.guess_type(image_path)
    return guessed or "image/jpeg"
