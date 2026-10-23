from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict

from google.cloud import vision


@dataclass
class VisionConfig:
    project: str | None = None
    location: str | None = None
    language_hints: str | None = None


def load_config() -> VisionConfig:
    return VisionConfig(
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION"),
        language_hints=os.getenv("VISION_LANGUAGE_HINTS"),
    )


def get_client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


def read_image_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()


def make_image(image_path: str) -> vision.Image:
    return vision.Image(content=read_image_bytes(image_path))


def to_dict_annotations(annotations: Any) -> Dict[str, Any]:
    return {"items": [getattr(a, "description", str(a)) for a in annotations or []]}
