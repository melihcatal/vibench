import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from google.cloud import vision


@dataclass
class VisionConfig:
    project_id: Optional[str] = None
    credentials_path: Optional[str] = None
    language_hints: Optional[list[str]] = None


def load_config() -> VisionConfig:
    hints = os.getenv("VISION_LANGUAGE_HINTS", "").strip()
    return VisionConfig(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT"),
        credentials_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        language_hints=[h for h in hints.split(",") if h] if hints else None,
    )


def client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


def image_from_bytes(image_bytes: bytes) -> vision.Image:
    return vision.Image(content=image_bytes)


def image_from_path(path: str) -> vision.Image:
    with open(path, "rb") as f:
        return vision.Image(content=f.read())


def image_from_uri(uri: str) -> vision.Image:
    return vision.Image(source=vision.ImageSource(image_uri=uri))


def image_input(source: str) -> vision.Image:
    if source.startswith("gs://") or source.startswith("http://") or source.startswith("https://"):
        return image_from_uri(source)
    return image_from_path(source)
