import base64
import os
from dataclasses import dataclass
from typing import Optional


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name, default)
    return value if value not in ("", None) else default


@dataclass
class VisionClientConfig:
    provider: str = "google-cloud-vision"
    credentials: Optional[str] = None


def load_vision_config() -> VisionClientConfig:
    return VisionClientConfig(credentials=_env("GOOGLE_APPLICATION_CREDENTIALS"))


def image_to_content(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()


def image_to_base64(image_path: str) -> str:
    return base64.b64encode(image_to_content(image_path)).decode("utf-8")


def require_image_path(image_path: str) -> str:
    if not image_path:
        raise ValueError("image_path is required")
    return image_path
