from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class VisionClientConfig:
    google_api_key: Optional[str] = None
    timeout_seconds: float = 30.0
    translate_api_key: Optional[str] = None
    gcs_bucket: Optional[str] = None
    gcs_project: Optional[str] = None


def load_vision_config() -> VisionClientConfig:
    return VisionClientConfig(
        google_api_key=os.getenv("GOOGLE_VISION_API_KEY") or os.getenv("GOOGLE_API_KEY"),
        timeout_seconds=float(os.getenv("VISION_TIMEOUT_SECONDS", "30")),
        translate_api_key=os.getenv("GOOGLE_TRANSLATE_API_KEY"),
        gcs_bucket=os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET"),
        gcs_project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    )


def build_image_data_uri(image_path: str) -> str:
    data = Path(image_path).read_bytes()
    encoded = base64.b64encode(data).decode("ascii")
    return f"data:image/*;base64,{encoded}"


__all__ = ["VisionClientConfig", "load_vision_config", "build_image_data_uri"]
