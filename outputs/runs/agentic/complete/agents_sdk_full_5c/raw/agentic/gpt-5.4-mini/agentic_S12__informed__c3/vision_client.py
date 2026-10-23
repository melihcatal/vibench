from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from google.cloud import vision


@dataclass
class VisionConfig:
    project: Optional[str] = os.getenv("GOOGLE_CLOUD_PROJECT")
    credentials: Optional[str] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    language_hint: str = os.getenv("VISION_LANGUAGE_HINT", "en")


def build_client() -> vision.ImageAnnotatorClient:
    # Google Cloud Vision client, identified by google.cloud.vision and GOOGLE_APPLICATION_CREDENTIALS.
    return vision.ImageAnnotatorClient()


def load_image_content(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()


def make_image(image_path: str) -> vision.Image:
    return vision.Image(content=load_image_content(image_path))
