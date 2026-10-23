import base64
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class VisionConfig:
    endpoint: Optional[str]
    api_key: Optional[str]
    language_hints: str


def load_vision_config() -> VisionConfig:
    return VisionConfig(
        endpoint=os.getenv("AZURE_VISION_ENDPOINT"),
        api_key=os.getenv("AZURE_VISION_KEY"),
        language_hints=os.getenv("VISION_LANGUAGE_HINTS", "en"),
    )


def image_to_data_uri(image_bytes: bytes, mime_type: str = "image/jpeg") -> str:
    encoded = base64.b64encode(image_bytes).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"
